"""Control-plane kernel: one handler table, 125 distinct contracts.

Agents are thin. The algorithms live here so the AGI tick can call them
without importing hyphenated directories.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from .control_catalog import AGENTS, BY_ID, AgentDef
from .envelope import SchemaError, new_id, utc_now

SECRET = b"h11c-control-plane-dev-secret"
INJECTION_MARKERS = (
    "ignore previous instructions",
    "ignore all previous",
    "</agent system instructions>",
    "<agent system instructions>",
    "you are now",
    "system prompt",
)

PHASES = ("PERCEIVE", "RETRIEVE", "REASON", "ALIGN", "ACT", "REMEMBER")


class ControlError(ValueError):
    pass


def _mac(payload: Any) -> str:
    blob = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hmac.new(SECRET, blob, hashlib.sha256).hexdigest()


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Process-global control state (one AGI instance owns one KernelState)
# ---------------------------------------------------------------------------

@dataclass
class KernelState:
    blackboard: Dict[str, Any] = field(default_factory=dict)
    goal_stack: List[str] = field(default_factory=list)
    schedule: List[Dict[str, Any]] = field(default_factory=list)
    audit: List[str] = field(default_factory=list)
    seen_nonces: set = field(default_factory=set)
    vault: Dict[str, str] = field(default_factory=dict)
    spines: Dict[str, List[str]] = field(default_factory=dict)
    halt: bool = False
    admitted: Dict[str, bool] = field(default_factory=dict)
    phase: str = "PERCEIVE"
    budget: int = 64
    identities: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.audit:
            self.audit.append(_sha("genesis"))
        if not self.spines:
            self.spines["host_infection"] = [
                "H11-ANATOMIA",
                "H11-PARASITOLOGIA",
                "H11-PHYSIOLOGIA",
                "H11-LONGTERM",
                "H11-REASON",
                "H11-ALIGN",
            ]


def remap_fields(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    mapping = agent.params.get("mapping") or {}
    src = payload.get("payload") or payload
    out: Dict[str, Any] = {}
    for src_key, dst in mapping.items():
        out[dst] = src.get(src_key)
    return {"payload": out, "mapped": list(mapping.values())}


def fuse_events(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    events = list(payload.get("events") or [])
    extra = payload.get("extra_events") or []
    merged = []
    seen = set()
    for e in events + list(extra):
        key = json.dumps(e, sort_keys=True, default=str) if not isinstance(e, str) else e
        if key in seen:
            continue
        seen.add(key)
        merged.append(e)
    return {"events": merged, "count": len(merged)}


def bind_role(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    role = agent.params.get("role", "bound")
    targets = list(agent.params.get("targets") or [])
    return {"bindings": {role: targets}, "case_id": (payload.get("case") or payload).get("case_id")}


def compose_pipeline(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    goal = payload.get("goal") or "general"
    caps = list(payload.get("capabilities") or agent.params.get("capabilities") or [])
    pipeline = list(caps)
    if "act" in goal.lower() or "treat" in goal.lower() or "medical" in goal.lower():
        if "H11-ALIGN" not in pipeline:
            pipeline.append("H11-ALIGN")
        if "H11C-ALIGN-ENFORCE" not in pipeline:
            pipeline.append("H11C-ALIGN-ENFORCE")
    return {"pipeline": pipeline, "goal": goal}


def check_contract(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    required = list(agent.params.get("required") or payload.get("required") or [])
    body = payload.get("payload") or payload
    missing = [k for k in required if k not in body]
    ok = not missing
    if not ok and agent.params.get("fail_closed", True):
        return {"ok": False, "missing": missing}
    return {"ok": ok, "missing": missing}


def coerce_types(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    types = agent.params.get("types") or payload.get("types") or {}
    body = dict(payload.get("payload") or payload)
    for key, typ in types.items():
        if key not in body:
            continue
        val = body[key]
        if typ == "float":
            body[key] = float(val)
        elif typ == "str":
            body[key] = str(val)
        elif typ == "list" and not isinstance(val, list):
            body[key] = [val]
    return {"payload": body}


def join_traces(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    traces = list(payload.get("traces") or [])
    traces.sort(key=lambda t: str((t or {}).get("ts") if isinstance(t, dict) else t))
    return {"trace": traces, "hops": len(traces)}


def project_memory(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    body = payload.get("payload") or payload
    trace = {
        "case_id": body.get("case_id"),
        "diagnosis": (body.get("diagnosis") or {}).get("identified_parasite")
        if isinstance(body.get("diagnosis"), dict)
        else body.get("diagnosis"),
        "sealed_at": utc_now(),
    }
    return {"trace": trace}


def inject_premises(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    body = payload.get("payload") or payload
    dx = body.get("diagnosis") or {}
    vitals = body.get("vitals") or {}
    premises = []
    if isinstance(dx, dict):
        if dx.get("identified_parasite"):
            premises.append(f"Identified parasite is {dx['identified_parasite']}.")
        if dx.get("recommended_antiparasitic"):
            premises.append(f"Recommended antiparasitic is {dx['recommended_antiparasitic']}.")
        if "confidence_score" in dx:
            premises.append(f"Diagnostic confidence is {dx['confidence_score']}.")
    if vitals.get("MeanArterialPressure") is not None:
        premises.append(f"Mean arterial pressure is {vitals['MeanArterialPressure']} mmHg.")
    if vitals.get("HeartRate") is not None:
        premises.append(f"Heart rate is {vitals['HeartRate']} bpm.")
    return {"premises": premises}


def attach_align(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    pipeline = list(payload.get("pipeline") or [])
    if "H11-ALIGN" not in pipeline:
        pipeline.append("H11-ALIGN")
    if "H11C-ALIGN-ENFORCE" not in pipeline:
        pipeline.append("H11C-ALIGN-ENFORCE")
    return {"pipeline": pipeline, "align_hooked": True}


def route_domain(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    case = payload.get("case") or payload
    forced = agent.params.get("domain")
    if forced:
        return {"domain": forced, "pipeline_id": agent.params.get("pipeline_id")}
    symptoms = case.get("symptoms") or []
    smear = case.get("blood_smear_density_per_ul")
    if smear or any("fever" in str(s).lower() for s in symptoms) or case.get("patient_id"):
        if smear or symptoms:
            return {"domain": "medical", "pipeline_id": "host_infection"}
    text = str(case.get("goal") or case.get("query") or "").lower()
    if any(w in text for w in ("contract", "statute", "court")):
        return {"domain": "legal", "pipeline_id": "legal_research"}
    if any(w in text for w in ("trade", "portfolio", "option")):
        return {"domain": "finance", "pipeline_id": "financial_analysis"}
    if any(w in text for w in ("circuit", "stress", "beam")):
        return {"domain": "engineering", "pipeline_id": "engineering_design"}
    if any(w in text for w in ("simulate", "hypothesis", "orbit")):
        return {"domain": "science", "pipeline_id": "scientific_model"}
    return {"domain": "general", "pipeline_id": "cognitive_loop"}


def pack_context(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    budget = int(payload.get("budget") or agent.params.get("budget") or 32)
    body = payload.get("payload") or payload
    keys = [k for k in body.keys() if k not in ("memory_embedding",)][:budget]
    context = {k: body[k] for k in keys}
    return {"context": context, "kept": len(keys)}


def reduce_results(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    body = payload.get("payload") or payload
    summary = {
        "case_id": body.get("case_id"),
        "domain": body.get("domain"),
        "allowed": body.get("allowed"),
        "diagnosis": body.get("diagnosis"),
    }
    return {"summary": summary}


def merge_conflicts(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    candidates = list(payload.get("candidates") or [])
    if not candidates:
        return {"chosen": None, "minority": []}
    def conf(c: Any) -> float:
        if isinstance(c, dict):
            return float(c.get("confidence") or c.get("confidence_score") or 0.0)
        return 0.0
    ranked = sorted(candidates, key=conf, reverse=True)
    chosen = ranked[0]
    minority = ranked[1:] if agent.params.get("keep_minority") else []
    return {"chosen": chosen, "minority": minority}


def map_capabilities(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    goal = str(payload.get("goal") or "").lower()
    caps = ["H11C-CONTRACT-CHECKER", "H11C-ZERO-TRUST-HOP"]
    if "medical" in goal or "patient" in goal or "treat" in goal:
        caps.extend(["H11C-MEDICAL-INTEGRATOR", "H11-ANATOMIA", "H11-PARASITOLOGIA", "H11-PHYSIOLOGIA", "H11-LONGTERM", "H11-REASON", "H11-ALIGN"])
    caps.append("H11C-ALIGN-ENFORCE")
    return {"capabilities": caps, "goal": goal}


def resolve_deps(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    nodes = list(payload.get("nodes") or [])
    edges = list(payload.get("edges") or [])
    if not nodes and edges:
        nodes = sorted({n for e in edges for n in e[:2]})
    incoming = {n: 0 for n in nodes}
    adj: Dict[str, List[str]] = {n: [] for n in nodes}
    for e in edges:
        a, b = e[0], e[1]
        if a in adj and b in incoming:
            adj[a].append(b)
            incoming[b] += 1
    ready = [n for n, d in incoming.items() if d == 0]
    order = []
    while ready:
        n = ready.pop(0)
        order.append(n)
        for m in adj[n]:
            incoming[m] -= 1
            if incoming[m] == 0:
                ready.append(m)
    if len(order) != len(nodes):
        raise ControlError("dependency cycle")
    return {"order": order}


def splice_external(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    kind = agent.params.get("kind", "external")
    body = dict(payload.get("payload") or payload)
    external = payload.get("external")
    if external is None:
        return {"payload": body, "spliced": False, "kind": kind}
    body[f"{kind}_input"] = external
    body[f"{kind}_cited"] = True
    return {"payload": body, "spliced": True, "kind": kind}


def register_spine(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    spine_id = payload.get("spine_id") or agent.params.get("spine_id")
    hops = list(payload.get("hops") or agent.params.get("hops") or [])
    agent.state.spines[spine_id] = hops
    return {"registry": dict(agent.state.spines), "spine_id": spine_id}


def cognitive_tick(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    if agent.state.halt:
        return {"state": "HALTED", "phase": agent.state.phase}
    force = agent.params.get("force_phase")
    if force:
        agent.state.phase = force
    idx = PHASES.index(agent.state.phase) if agent.state.phase in PHASES else 0
    current = PHASES[idx]
    if current == "ACT" and not payload.get("align_allowed"):
        raise ControlError("ACT without ALIGN is illegal")
    nxt = PHASES[(idx + 1) % len(PHASES)]
    agent.state.phase = nxt
    return {"state": current, "next": nxt, "sleep": bool(agent.params.get("sleep"))}


def goal_stack(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    op = payload.get("op") or agent.params.get("op") or "peek"
    if op == "push":
        agent.state.goal_stack.append(str(payload.get("goal") or agent.params.get("kind") or "goal"))
    elif op == "pop" and agent.state.goal_stack:
        agent.state.goal_stack.pop()
    return {"stack": list(agent.state.goal_stack), "op": op}


def schedule(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    item = payload.get("item")
    queue = list(payload.get("queue") or agent.state.schedule)
    if item:
        priority = int(item.get("priority", 0)) if isinstance(item, dict) else 0
        if "safety" in str(item).lower() or (isinstance(item, dict) and item.get("safety")):
            priority += 100
        record = item if isinstance(item, dict) else {"item": item, "priority": priority}
        record = dict(record)
        record["priority"] = priority
        queue.append(record)
        queue.sort(key=lambda x: -int(x.get("priority", 0)))
    agent.state.schedule = queue
    return {"queue": queue}


def route(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    pipeline = list(payload.get("pipeline") or [])
    index = int(payload.get("index") or 0)
    if index < 0 or index >= len(pipeline):
        return {"next_agent": None, "done": True}
    return {"next_agent": pipeline[index], "done": False, "index": index}


def run_workflow(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    return resolve_deps(agent, payload)


def state_machine(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    state = payload.get("state") or "admitted"
    event = payload.get("event") or "tick"
    table = {
        ("admitted", "bind"): "bound",
        ("bound", "run"): "running",
        ("running", "align"): "aligned",
        ("aligned", "act"): "acted",
        ("acted", "seal"): "sealed",
        ("running", "halt"): "halted",
        ("aligned", "replan"): "running",
    }
    nxt = table.get((state, event), state)
    if event == "act" and state != "aligned":
        raise ControlError("state machine refused ACT before ALIGN")
    return {"state": nxt, "event": event}


def blackboard(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    ns = agent.params.get("namespace", "default")
    op = payload.get("op") or "get"
    key = f"{ns}:{payload.get('key')}"
    if op == "set":
        agent.state.blackboard[key] = payload.get("value")
    val = agent.state.blackboard.get(key)
    return {"board": {key: val}, "op": op}


def allocate(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    candidates = list(payload.get("candidates") or [])
    scores = list(payload.get("scores") or [])
    if not candidates:
        return {"chosen": None}
    if len(scores) < len(candidates):
        scores = scores + [0.0] * (len(candidates) - len(scores))
    chosen = candidates[max(range(len(candidates)), key=lambda i: scores[i])]
    return {"chosen": chosen}


def budget(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    remaining = int(payload.get("budget") if payload.get("budget") is not None else agent.state.budget)
    cost = int(payload.get("cost") or 1)
    remaining -= cost
    agent.state.budget = remaining
    if remaining <= 0:
        agent.state.halt = True
    return {"budget": remaining, "halt": remaining <= 0, "shed": bool(agent.params.get("shed"))}


def timeout(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    elapsed = float(payload.get("elapsed") or 0)
    deadline = float(payload.get("deadline") or 1.0)
    return {"expired": elapsed > deadline, "elapsed": elapsed, "deadline": deadline}


def retry(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    if payload.get("halted"):
        return {"retry": False, "reason": "halt_is_not_retriable"}
    attempts = int(payload.get("attempts") or 0)
    max_attempts = int(payload.get("max_attempts") or 3)
    return {"retry": attempts < max_attempts, "attempts": attempts}


def fallback(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    if payload.get("primary_ok"):
        return {"pipeline_id": payload.get("primary_id") or "primary"}
    return {"pipeline_id": payload.get("fallback_id") or "cognitive_loop"}


def fanout(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    n = int(payload.get("n") or 2)
    return {"branches": [f"b{i}" for i in range(n)], "n": n}


def join(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    branches = list(payload.get("branches") or [])
    expected = int(payload.get("expected") or len(branches))
    return {"joined": len(branches) >= expected, "count": len(branches)}


def preempt(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    running = int(payload.get("running") or 0)
    incoming = int(payload.get("incoming_priority") or 0)
    nmi = bool(agent.params.get("nmi"))
    return {"preempt": nmi or incoming > running, "boost": bool(agent.params.get("boost"))}


def halt(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    agent.state.halt = True
    return {"state": "HALTED", "quarantine": bool(agent.params.get("quarantine"))}


def resume(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    if not payload.get("admitted"):
        raise ControlError("resume requires admission")
    if not payload.get("checkpoint"):
        raise ControlError("resume requires checkpoint")
    agent.state.halt = False
    return {"state": "RESUMED"}


def checkpoint(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    snap = {
        "phase": agent.state.phase,
        "budget": agent.state.budget,
        "halt": agent.state.halt,
        "ts": utc_now(),
    }
    return {"checkpoint": snap, "mac": _mac(snap)}


def run_pipeline(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    pipeline_id = payload.get("pipeline_id") or "host_infection"
    hops = agent.state.spines.get(pipeline_id) or []
    return {"pipeline_id": pipeline_id, "hops": hops, "payload": payload.get("payload") or payload}


def agi_tick(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"queued": True, "case": payload.get("case") or payload}


def identity(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    name = str(payload.get("name") or "anon")
    ident = agent.state.identities.get(name) or new_id("id")
    agent.state.identities[name] = ident
    return {"identity": ident, "name": name}


def capability(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    ident = payload.get("identity") or "anon"
    scopes = list(payload.get("scopes") or ["read"])
    body = json.dumps({"identity": ident, "scopes": scopes}, sort_keys=True)
    token = {"body": body, "sig": hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest()}
    return {"token": token, "scopes": scopes}


def sandbox(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    hop = payload.get("hop") or "unknown"
    return {"sandboxed": True, "hop": hop}


def injection(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    text = str(payload.get("text") or "").lower()
    dirty = any(m in text for m in INJECTION_MARKERS)
    return {"clean": not dirty, "dirty": dirty}


def allowlist(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    item = payload.get("item")
    allowed = set(payload.get("allowed") or agent.params.get("allowed") or [])
    if not allowed:
        allowed = set(BY_ID.keys()) | {
            "H11-ANATOMIA",
            "H11-PARASITOLOGIA",
            "H11-PHYSIOLOGIA",
            "H11-LONGTERM",
            "H11-REASON",
            "H11-ALIGN",
        }
    return {"ok": item in allowed, "item": item}


def classify(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    body = payload.get("payload") or payload
    if body.get("patient_id") or body.get("symptoms") or body.get("diagnosis"):
        label = "medical"
    elif body.get("secret"):
        label = "secret"
    else:
        label = "internal"
    return {"label": label}


def compartment(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    label = payload.get("label") or "internal"
    sink = payload.get("sink") or "internal"
    illegal = (label == "medical" and sink == "public") or (label == "secret" and sink != "secret")
    return {"ok": not illegal, "label": label, "sink": sink}


def audit(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    prev = agent.state.audit[-1]
    event = json.dumps(payload.get("event") or payload, sort_keys=True, default=str)
    head = _sha(prev + event)
    agent.state.audit.append(head)
    return {"head": head, "length": len(agent.state.audit)}


def rate_limit(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    tokens = int(payload.get("tokens") or 1)
    return {"ok": tokens > 0, "tokens": max(0, tokens - 1)}


def privilege(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    scopes = list(payload.get("scopes") or [])
    drop = list(payload.get("drop") or agent.params.get("drop") or [])
    next_scopes = [s for s in scopes if s not in drop]
    if len(next_scopes) > len(scopes):
        raise ControlError("scopes cannot increase")
    return {"scopes": next_scopes}


def redact(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    body = dict(payload.get("payload") or payload)
    keys = list(payload.get("keys") or agent.params.get("keys") or ["secret"])
    for k in keys:
        if k in body:
            body[k] = "[REDACTED]"
    return {"payload": body}


def sanitize(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    text = str(payload.get("text") or "")
    text = re.sub(r"</?agent system instructions>", "", text, flags=re.I)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    return {"text": text.strip()}


def policy(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    attrs = payload.get("attrs") or {}
    if agent.params.get("rules"):
        if attrs.get("align_allowed") is False:
            return {"decision": "deny", "reason": "align_not_allowed"}
        if "confidence" in (agent.params["rules"][0].get("require") or []) and float(attrs.get("confidence") or 0) < 0.85:
            return {"decision": "deny", "reason": "low_confidence"}
    return {"decision": "allow"}


def consent(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"ok": bool(payload.get("consent"))}


def dual(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    need = int(payload.get("need") or agent.params.get("need") or 2)
    approvals = list(payload.get("approvals") or [])
    return {"ok": len(set(approvals)) >= need, "need": need}


def mac(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    body = payload.get("payload") or payload
    return {"mac": _mac(body)}


def replay(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    nonce = str(payload.get("nonce") or "")
    if not nonce:
        return {"ok": False, "reason": "missing_nonce"}
    if nonce in agent.state.seen_nonces:
        return {"ok": False, "reason": "replay"}
    agent.state.seen_nonces.add(nonce)
    return {"ok": True}


def vault(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    op = payload.get("op") or "has"
    key = str(payload.get("key") or "")
    if op == "put":
        agent.state.vault[key] = str(payload.get("value") or "")
        return {"ok": True, "stored": True}
    if op == "has":
        return {"ok": key in agent.state.vault}
    if op == "get":
        raise ControlError("vault never returns secrets into the envelope")
    return {"ok": False}


def zero_trust(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    ok = all(
        [
            bool(payload.get("identity")),
            bool(payload.get("token")),
            payload.get("sandboxed") is True,
            payload.get("schema_ok") is True,
        ]
    )
    return {"ok": ok}


def align_enforce(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    would_act = bool(payload.get("would_act"))
    allowed = bool(payload.get("align_allowed"))
    if would_act and not allowed:
        agent.state.halt = True
        return {"ok": False, "reason": "align_skipped_or_denied"}
    return {"ok": True}


def license(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    flags = payload.get("ok_flags") or {}
    licensed = all(bool(flags.get(k)) for k in ("align", "sandbox", "policy")) if flags else False
    if not flags:
        licensed = bool(payload.get("align_allowed") and payload.get("sandboxed") and payload.get("policy") == "allow")
    return {"licensed": licensed}


def admit(agent: "ControlAgent", payload: Dict[str, Any]) -> Dict[str, Any]:
    case = payload.get("case") or payload
    case_id = case.get("case_id") or new_id("case")
    ok = bool(case.get("patient_id") or case.get("goal") or case.get("query"))
    agent.state.admitted[case_id] = ok
    return {"admitted": ok, "case_id": case_id}


HANDLERS: Dict[str, Callable[["ControlAgent", Dict[str, Any]], Dict[str, Any]]] = {
    "remap_fields": remap_fields,
    "fuse_events": fuse_events,
    "bind_role": bind_role,
    "compose_pipeline": compose_pipeline,
    "check_contract": check_contract,
    "coerce_types": coerce_types,
    "join_traces": join_traces,
    "project_memory": project_memory,
    "inject_premises": inject_premises,
    "attach_align": attach_align,
    "route_domain": route_domain,
    "pack_context": pack_context,
    "reduce_results": reduce_results,
    "merge_conflicts": merge_conflicts,
    "map_capabilities": map_capabilities,
    "resolve_deps": resolve_deps,
    "splice_external": splice_external,
    "register_spine": register_spine,
    "cognitive_tick": cognitive_tick,
    "goal_stack": goal_stack,
    "schedule": schedule,
    "route": route,
    "run_workflow": run_workflow,
    "state_machine": state_machine,
    "blackboard": blackboard,
    "allocate": allocate,
    "budget": budget,
    "timeout": timeout,
    "retry": retry,
    "fallback": fallback,
    "fanout": fanout,
    "join": join,
    "preempt": preempt,
    "halt": halt,
    "resume": resume,
    "checkpoint": checkpoint,
    "run_pipeline": run_pipeline,
    "agi_tick": agi_tick,
    "identity": identity,
    "capability": capability,
    "sandbox": sandbox,
    "injection": injection,
    "allowlist": allowlist,
    "classify": classify,
    "compartment": compartment,
    "audit": audit,
    "rate_limit": rate_limit,
    "privilege": privilege,
    "redact": redact,
    "sanitize": sanitize,
    "policy": policy,
    "consent": consent,
    "dual": dual,
    "mac": mac,
    "replay": replay,
    "vault": vault,
    "zero_trust": zero_trust,
    "align_enforce": align_enforce,
    "license": license,
    "admit": admit,
}


@dataclass
class ControlAgent:
    agent_id: str
    state: KernelState = field(default_factory=KernelState)

    def __post_init__(self) -> None:
        if self.agent_id not in BY_ID:
            raise ControlError(f"unknown control agent {self.agent_id}")
        self.spec: AgentDef = BY_ID[self.agent_id]
        self.params = dict(self.spec.params)

    def process(self, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = dict(payload or {})
        handler = HANDLERS.get(self.spec.handler)
        if handler is None:
            raise ControlError(f"no handler {self.spec.handler}")
        result = handler(self, payload)
        result["agent_id"] = self.agent_id
        result["family"] = self.spec.family
        result["handler"] = self.spec.handler
        result["ts"] = utc_now()
        return result


def make_agent(agent_id: str, state: Optional[KernelState] = None) -> ControlAgent:
    return ControlAgent(agent_id, state=state or KernelState())
