"""Compile heterogeneous specialist contracts into validated call arguments.

The repository contains multiple generations of agent contracts.  Runtime
Python signatures remain authoritative; adjacent JSON schemas contribute
diagnostics and field declarations.  Values are copied from the admitted case
or blackboard only—this module never invents required inputs.
"""
from __future__ import annotations

import collections.abc
import dataclasses
import inspect
import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple, get_args, get_origin, get_type_hints

from ..case.blackboard import Blackboard
from ..loader import ROOT


class ContractCompilationError(ValueError):
    """Raised when required, evidence-backed inputs cannot be compiled."""

    def __init__(
        self,
        missing: Sequence[str],
        diagnostics: Optional["ContractDiagnostics"] = None,
        message: str = "",
    ) -> None:
        self.missing = list(missing)
        self.diagnostics = diagnostics
        detail = message or ("missing required specialist inputs: " + ", ".join(self.missing))
        super().__init__(detail)


@dataclass
class ContractDiagnostics:
    input_type: str = "mapping"
    bound_fields: List[str] = field(default_factory=list)
    field_provenance: Dict[str, str] = field(default_factory=dict)
    missing_required: List[str] = field(default_factory=list)
    schema_declared_fields: List[str] = field(default_factory=list)
    schema_required_fields: List[str] = field(default_factory=list)
    signature_only_fields: List[str] = field(default_factory=list)
    schema_only_fields: List[str] = field(default_factory=list)
    coercions: List[str] = field(default_factory=list)
    validation_errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@dataclass
class CompiledCall:
    args: List[Any]
    kwargs: Dict[str, Any]
    diagnostics: ContractDiagnostics


class SpecialistContractCompiler:
    """Normalizes case state into a specialist's declared callable contract."""

    # Aliases are directional and conservative. Each value must still exist in
    # the admitted case or blackboard, and is type-checked before use.
    FIELD_ALIASES: Dict[str, Tuple[str, ...]] = {
        "problem_statement": ("query", "goal", "objective"),
        "query": ("problem_statement", "goal", "objective"),
        "temperature_c": ("temp_c", "patient_vitals.temp_c"),
        "heart_rate": ("patient_vitals.heart_rate", "pulse_bpm"),
        "respiratory_rate": ("patient_vitals.respiratory_rate", "respirations_per_min"),
        "mean_arterial_pressure": ("patient_vitals.mean_arterial_pressure", "map_mm_hg"),
        "oxygenation_pao2": ("patient_vitals.oxygenation_pao2", "pao2_mm_hg"),
        "age_years": ("age", "patient.age_years"),
        "weight_kg": ("weight", "patient.weight_kg"),
        "height_m": ("height", "patient.height_m"),
        "t1_time_us": ("t1_us", "coherence_times.t1_us"),
        "t2_time_us": ("t2_us", "coherence_times.t2_us"),
        "logits": ("scores", "values"),
        "premises": ("facts",),
    }

    def compile(
        self,
        method: Callable[..., Any],
        case: Mapping[str, Any],
        blackboard: Blackboard,
        relative_agent_path: str = "",
    ) -> CompiledCall:
        context, provenance = self._build_context(case, blackboard)
        schema = self._load_adjacent_schema(relative_agent_path)
        schema_fields, schema_required = self._schema_fields(schema)
        signature = inspect.signature(method)
        parameters = [
            parameter for parameter in signature.parameters.values()
            if parameter.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
        ]
        try:
            hints = get_type_hints(method)
        except Exception:
            hints = {}

        diagnostics = ContractDiagnostics(
            schema_declared_fields=sorted(schema_fields),
            schema_required_fields=sorted(schema_required),
        )

        if len(parameters) == 1:
            parameter = parameters[0]
            annotation = hints.get(parameter.name, parameter.annotation)
            dataclass_type = self._find_dataclass_type(annotation)
            if dataclass_type is not None:
                diagnostics.input_type = dataclass_type.__name__
                value = self._compile_dataclass(dataclass_type, context, provenance, diagnostics)
                self._add_schema_diagnostics(diagnostics, {f.name for f in dataclasses.fields(dataclass_type)})
                return CompiledCall([value], {}, diagnostics)
            if annotation is str or "json" in parameter.name.lower():
                diagnostics.input_type = "json"
                payload = {
                    "problem_statement": context.get("problem_statement", ""),
                    "premises": context.get("premises", []),
                    "reasoning_mode": context.get("reasoning_mode", "deduction"),
                }
                diagnostics.bound_fields = sorted(payload)
                diagnostics.field_provenance = {
                    key: provenance.get(key, "runtime-derived") for key in payload
                }
                return CompiledCall([json.dumps(payload)], {}, diagnostics)

            diagnostics.input_type = "mapping"
            diagnostics.bound_fields = sorted(context)
            diagnostics.field_provenance = {key: provenance[key] for key in context if key in provenance}
            return CompiledCall([context], {}, diagnostics)

        kwargs: Dict[str, Any] = {}
        signature_fields: set[str] = set()
        for parameter in parameters:
            signature_fields.add(parameter.name)
            annotation = hints.get(parameter.name, parameter.annotation)
            found, value, source = self._lookup(parameter.name, context, provenance)
            if found:
                try:
                    kwargs[parameter.name] = self._coerce(value, annotation, parameter.name, diagnostics)
                except (TypeError, ValueError) as exc:
                    diagnostics.validation_errors.append(str(exc))
                diagnostics.field_provenance[parameter.name] = source
            elif parameter.default is inspect.Parameter.empty:
                diagnostics.missing_required.append(parameter.name)

        diagnostics.bound_fields = sorted(kwargs)
        self._add_schema_diagnostics(diagnostics, signature_fields)
        if diagnostics.validation_errors:
            raise ContractCompilationError([], diagnostics, "; ".join(diagnostics.validation_errors))
        if diagnostics.missing_required:
            raise ContractCompilationError(diagnostics.missing_required, diagnostics)
        return CompiledCall([], kwargs, diagnostics)

    def _compile_dataclass(
        self,
        dataclass_type: type,
        context: Mapping[str, Any],
        provenance: Mapping[str, str],
        diagnostics: ContractDiagnostics,
    ) -> Any:
        values: Dict[str, Any] = {}
        try:
            field_hints = get_type_hints(dataclass_type)
        except Exception:
            field_hints = {}
        for declared in dataclasses.fields(dataclass_type):
            found, value, source = self._lookup(declared.name, context, provenance)
            if found:
                annotation = field_hints.get(declared.name, declared.type)
                try:
                    values[declared.name] = self._coerce(value, annotation, declared.name, diagnostics)
                except (TypeError, ValueError) as exc:
                    diagnostics.validation_errors.append(str(exc))
                diagnostics.field_provenance[declared.name] = source
            elif declared.default is dataclasses.MISSING and declared.default_factory is dataclasses.MISSING:
                diagnostics.missing_required.append(declared.name)
        diagnostics.bound_fields = sorted(values)
        if diagnostics.validation_errors:
            raise ContractCompilationError([], diagnostics, "; ".join(diagnostics.validation_errors))
        if diagnostics.missing_required:
            raise ContractCompilationError(diagnostics.missing_required, diagnostics)
        return dataclass_type(**values)

    def _build_context(
        self,
        case: Mapping[str, Any],
        blackboard: Blackboard,
    ) -> Tuple[Dict[str, Any], Dict[str, str]]:
        context = dict(case)
        provenance = {str(key): f"case.{key}" for key in case}
        leaf_values: Dict[str, List[Tuple[str, Any]]] = {}

        def visit(value: Any, path: str) -> None:
            if not isinstance(value, Mapping):
                return
            for key, child in value.items():
                child_path = f"{path}.{key}" if path else str(key)
                context.setdefault(child_path, child)
                provenance.setdefault(child_path, f"case.{child_path}")
                leaf_values.setdefault(str(key), []).append((child_path, child))
                visit(child, child_path)

        visit(case, "")
        for leaf, occurrences in leaf_values.items():
            if leaf not in context and len(occurrences) == 1:
                path, value = occurrences[0]
                context[leaf] = value
                provenance[leaf] = f"case.{path}"

        facts: Dict[str, Any] = {}
        for key, item in blackboard.facts.items():
            value = item.get("value") if isinstance(item, Mapping) else item
            facts[key] = value
            if key not in context:
                context[key] = value
                provenance[key] = f"blackboard.{key}"
        context["blackboard_facts"] = facts
        provenance["blackboard_facts"] = "blackboard"

        context.setdefault("problem_statement", str(case.get("query") or case.get("goal") or ""))
        provenance.setdefault("problem_statement", "runtime-derived-from-case")
        premises = list(case.get("premises") or [])
        premises.extend(
            str(item.get("snippet") or item.get("title") or "")
            for item in case.get("retrieved_evidence") or []
            if isinstance(item, Mapping) and (item.get("snippet") or item.get("title"))
        )
        context.setdefault("premises", premises)
        provenance.setdefault("premises", "case.premises+retrieved_evidence")
        context.setdefault("reasoning_mode", "deduction")
        provenance.setdefault("reasoning_mode", "runtime-default")
        return context, provenance

    def _lookup(
        self,
        field_name: str,
        context: Mapping[str, Any],
        provenance: Mapping[str, str],
    ) -> Tuple[bool, Any, str]:
        candidates = (field_name,) + self.FIELD_ALIASES.get(field_name, ())
        for candidate in candidates:
            if candidate in context and context[candidate] is not None:
                return True, context[candidate], provenance.get(candidate, f"case.{candidate}")
        return False, None, ""

    def _coerce(
        self,
        value: Any,
        annotation: Any,
        field_name: str,
        diagnostics: ContractDiagnostics,
    ) -> Any:
        if annotation in (Any, inspect.Parameter.empty, None):
            return value
        origin = get_origin(annotation)
        args = get_args(annotation)
        if origin is not None and type(None) in args:
            non_none = [arg for arg in args if arg is not type(None)]
            return self._coerce(value, non_none[0] if len(non_none) == 1 else Any, field_name, diagnostics)
        if inspect.isclass(annotation) and dataclasses.is_dataclass(annotation):
            if isinstance(value, annotation):
                return value
            if not isinstance(value, Mapping):
                raise TypeError(f"{field_name} must be an object for {annotation.__name__}")
            nested_context = dict(value)
            nested_provenance = {key: f"{field_name}.{key}" for key in nested_context}
            return self._compile_dataclass(annotation, nested_context, nested_provenance, diagnostics)
        if inspect.isclass(annotation) and issubclass(annotation, Enum):
            if isinstance(value, annotation):
                return value
            for member in annotation:
                if str(value).lower() in (member.name.lower(), str(member.value).lower()):
                    diagnostics.coercions.append(f"{field_name}: enum")
                    return member
            raise TypeError(f"{field_name} is not a valid {annotation.__name__}")
        if origin in (list, List, Sequence, collections.abc.Sequence):
            if isinstance(value, (str, bytes)) or not isinstance(value, collections.abc.Sequence):
                raise TypeError(f"{field_name} must be a sequence")
            item_type = args[0] if args else Any
            return [self._coerce(item, item_type, field_name, diagnostics) for item in value]
        if origin in (dict, Dict, Mapping, collections.abc.Mapping):
            if not isinstance(value, Mapping):
                raise TypeError(f"{field_name} must be an object")
            return dict(value)
        if annotation is float and isinstance(value, (int, float)) and not isinstance(value, bool):
            if not isinstance(value, float):
                diagnostics.coercions.append(f"{field_name}: int->float")
            return float(value)
        if annotation is int and isinstance(value, int) and not isinstance(value, bool):
            return value
        if annotation is bool and isinstance(value, bool):
            return value
        if annotation is str and isinstance(value, str):
            return value
        if isinstance(annotation, type) and isinstance(value, annotation):
            return value
        raise TypeError(f"{field_name} has incompatible type {type(value).__name__} for {annotation}")

    @staticmethod
    def _find_dataclass_type(annotation: Any) -> Optional[type]:
        if inspect.isclass(annotation) and dataclasses.is_dataclass(annotation):
            return annotation
        for candidate in get_args(annotation) if get_origin(annotation) is not None else ():
            if inspect.isclass(candidate) and dataclasses.is_dataclass(candidate):
                return candidate
        return None

    @staticmethod
    def _load_adjacent_schema(relative_agent_path: str) -> Dict[str, Any]:
        if not relative_agent_path:
            return {}
        relative = Path(relative_agent_path)
        if relative.is_absolute() or ".." in relative.parts:
            return {}
        path = (ROOT / relative).with_name("schema.json")
        try:
            return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
        except (OSError, ValueError):
            return {}

    @staticmethod
    def _schema_fields(schema: Mapping[str, Any]) -> Tuple[set[str], set[str]]:
        properties = schema.get("properties")
        if isinstance(properties, Mapping):
            declared = {str(key) for key in properties}
            required = {str(key) for key in schema.get("required", [])}
            return declared, required
        inputs = schema.get("inputs")
        if isinstance(inputs, list):
            declared = {
                str(item["name"]) for item in inputs
                if isinstance(item, Mapping) and item.get("name")
            }
            required = {
                str(item["name"]) for item in inputs
                if isinstance(item, Mapping) and item.get("name") and item.get("required", True)
            }
            return declared, required
        return set(), set()

    @staticmethod
    def _add_schema_diagnostics(diagnostics: ContractDiagnostics, signature_fields: set[str]) -> None:
        schema_fields = set(diagnostics.schema_declared_fields)
        diagnostics.signature_only_fields = sorted(signature_fields - schema_fields)
        diagnostics.schema_only_fields = sorted(schema_fields - signature_fields)
