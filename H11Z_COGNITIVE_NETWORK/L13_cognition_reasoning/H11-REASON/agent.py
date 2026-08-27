import json
import logging
import re
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum, auto

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("H11-REASON")

class ReasoningMode(Enum):
    DEDUCTION = auto()
    INDUCTION = auto()
    ABDUCTION = auto()
    PROBABILISTIC = auto()

@dataclass
class LogicPremise:
    id: str
    content: str
    truth_value: float = 1.0
    is_axiom: bool = False

@dataclass
class InferenceStep:
    step_id: str
    premises_used: List[str]
    inferred_content: str
    confidence: float
    reasoning_type: ReasoningMode

@dataclass
class InferenceChain:
    chain_id: str
    steps: List[InferenceStep] = field(default_factory=list)
    overall_confidence: float = 1.0

    def add_step(self, step: InferenceStep):
        self.steps.append(step)
        # Simple joint probability assumption for confidence
        self.overall_confidence *= step.confidence

class CognitiveSubstrate:
    """Provides a foundational substrate for compositional logic."""
    
    def __init__(self, mode: ReasoningMode):
        self.mode = mode
        self.knowledge_base: Dict[str, LogicPremise] = {}

    def ingest_premise(self, premise: LogicPremise):
        self.knowledge_base[premise.id] = premise

    def evaluate_consistency(self) -> float:
        texts = [p.content.lower().strip().rstrip(".") for p in self.knowledge_base.values()]
        for t in texts:
            if t.startswith("not "):
                if any(other == t[4:] for other in texts):
                    return 0.4
            elif any(other == "not " + t for other in texts):
                return 0.4
        return 1.0 if self.knowledge_base else 0.0

    @staticmethod
    def _stem(word: str) -> str:
        w = word.lower().strip()
        irregular = {"men": "man", "women": "woman", "people": "person", "mice": "mouse"}
        w = irregular.get(w, w)
        if w.endswith("ses"):
            return w[:-2]
        if w.endswith("ies") and len(w) > 4:
            return w[:-3] + "y"
        if w.endswith("s") and not w.endswith("ss") and len(w) > 3:
            return w[:-1]
        return w

    def modus_ponens(self) -> List[str]:
        """All X are Y + Z is (a) X → Z is Y."""
        universals: List[Tuple[str, str]] = []
        particulars: List[Tuple[str, str]] = []
        for p in self.knowledge_base.values():
            text = p.content.strip().rstrip(".")
            m = re.match(r"^All (.+) are (.+)$", text, re.I)
            if m:
                universals.append((m.group(1).lower(), m.group(2).lower()))
                continue
            m = re.match(r"^(.+?) is (?:a |an )?(.+)$", text, re.I)
            if m:
                particulars.append((m.group(1).strip(), m.group(2).lower()))
        out: List[str] = []
        for subj, pred in particulars:
            pred_n = self._stem(pred)
            for xs, ys in universals:
                if pred == xs or pred_n == self._stem(xs):
                    out.append(f"{subj} is {ys}.")
        return out

class H11ReasonAgent:
    """Core agent for structured multi-step reasoning."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.active_chains: List[InferenceChain] = []

    def setup_context(self, premises: List[str], mode_str: str) -> CognitiveSubstrate:
        mode_map = {
            "deduction": ReasoningMode.DEDUCTION,
            "induction": ReasoningMode.INDUCTION,
            "abduction": ReasoningMode.ABDUCTION,
            "probabilistic": ReasoningMode.PROBABILISTIC
        }
        mode = mode_map.get(mode_str.lower(), ReasoningMode.DEDUCTION)
        substrate = CognitiveSubstrate(mode=mode)
        
        for i, p in enumerate(premises):
            substrate.ingest_premise(LogicPremise(id=f"P{i}", content=p, is_axiom=True))
            
        return substrate

    def perform_reasoning(self, problem: str, substrate: CognitiveSubstrate) -> InferenceChain:
        logger.info(f"Agent {self.agent_id} starting reasoning for: {problem}")
        chain = InferenceChain(chain_id=f"chain_{abs(hash(problem)) % 10**12}")
        facts = {p.content for p in substrate.knowledge_base.values()}

        deduced = substrate.modus_ponens()
        if deduced:
            chain.add_step(InferenceStep(
                "MP1",
                list(substrate.knowledge_base.keys()),
                "Modus ponens: " + " ".join(deduced),
                0.99,
                ReasoningMode.DEDUCTION,
            ))
            chain.add_step(InferenceStep(
                "MP2",
                ["MP1"],
                deduced[0],
                0.98,
                ReasoningMode.DEDUCTION,
            ))
            self.active_chains.append(chain)
            return chain

        medical = self._medical_decision(list(facts), problem)
        if medical:
            action, conclusion, conf = medical
            chain.add_step(InferenceStep(
                "M1",
                list(substrate.knowledge_base.keys()),
                f"Clinical facts bound. Proposed action: {action}.",
                0.97,
                ReasoningMode.DEDUCTION,
            ))
            chain.add_step(InferenceStep(
                "M2",
                ["M1"],
                conclusion,
                conf,
                ReasoningMode.DEDUCTION,
            ))
            self.active_chains.append(chain)
            return chain

        recalled = self._answer_from_facts(list(facts), problem)
        if recalled:
            action, conclusion, conf = recalled
            chain.add_step(InferenceStep(
                "R1",
                list(substrate.knowledge_base.keys()),
                f"Recalled facts applied. Action: {action}.",
                0.96,
                ReasoningMode.DEDUCTION,
            ))
            chain.add_step(InferenceStep(
                "R2",
                ["R1"],
                conclusion,
                conf,
                ReasoningMode.DEDUCTION,
            ))
            self.active_chains.append(chain)
            return chain

        joined = " | ".join(sorted(facts))
        chain.add_step(InferenceStep(
            "G1",
            list(substrate.knowledge_base.keys()),
            f"No rule fired. Open question: {problem} Given: {joined}",
            0.55,
            substrate.mode,
        ))
        self.active_chains.append(chain)
        return chain

    def _extract_clinical(self, facts: List[str], problem: str) -> Dict[str, Any]:
        blob = " ".join(facts) + " " + problem
        out: Dict[str, Any] = {}
        m = re.search(r"Identified parasite is ([^.]+)", blob)
        if m:
            out["parasite"] = m.group(1).strip()
        m = re.search(r"Recommended antiparasitic is ([^.]+)", blob)
        if m:
            out["drug"] = m.group(1).strip()
        m = re.search(r"Diagnostic confidence is ([0-9]+(?:\.[0-9]+)?)", blob)
        if m:
            out["conf"] = float(m.group(1))
        m = re.search(r"Mean arterial pressure is ([0-9]+(?:\.[0-9]+)?)", blob)
        if m:
            out["map_mmhg"] = float(m.group(1))
        return out

    def _treat_intent(self, problem: str) -> bool:
        p = problem.lower()
        return any(
            w in p
            for w in (
                "treat",
                "proceed with",
                "prescribe",
                "antiparasitic",
                "therapy",
                "should the host",
            )
        )

    def _medical_decision(self, facts: List[str], problem: str) -> Optional[Tuple[str, str, float]]:
        if not self._treat_intent(problem):
            return None
        cx = self._extract_clinical(facts, problem)
        parasite = cx.get("parasite")
        if not parasite:
            return None
        map_mmhg = cx.get("map_mmhg")
        conf = cx.get("conf")
        drug = cx.get("drug")
        if map_mmhg is not None and map_mmhg <= 40.0:
            return (
                "WITHHOLD",
                f"WITHHOLD treatment for {parasite}: MAP {map_mmhg} mmHg is critical.",
                0.99,
            )
        if conf is not None and conf < 0.85:
            return (
                "WITHHOLD",
                f"WITHHOLD treatment for {parasite}: confidence {conf} is below 0.85.",
                0.9,
            )
        if drug:
            return (
                "TREAT",
                f"TREAT {parasite} with {drug} (confidence {conf if conf is not None else 'n/a'}).",
                conf or 0.9,
            )
        return (
            "INVESTIGATE",
            f"INVESTIGATE {parasite}: no named protocol in premises.",
            0.6,
        )

    def _answer_from_facts(self, facts: List[str], problem: str) -> Optional[Tuple[str, str, float]]:
        cx = self._extract_clinical(facts, problem)
        p = problem.lower()
        parasite = cx.get("parasite")
        drug = cx.get("drug")
        if parasite and any(w in p for w in ("parasite", "organism", "diagnos", "infection", "what")):
            return ("ANSWER", f"The identified parasite is {parasite}.", 0.95)
        if drug and any(w in p for w in ("drug", "protocol", "medicine", "treat")):
            return ("ANSWER", f"The named protocol is {drug}.", 0.93)
        return None

    def assess_quality(self, chain: InferenceChain) -> Dict[str, Any]:
        """Evaluates the quality and soundness of a reasoning chain."""
        quality_score = chain.overall_confidence
        return {
            "is_sound": quality_score > 0.8,
            "quality_score": quality_score,
            "num_steps": len(chain.steps)
        }

    def process(self, request_json: str) -> str:
        try:
            req = json.loads(request_json)
            problem = req.get("problem_statement", "")
            premises = req.get("premises", [])
            mode = req.get("reasoning_mode", "deduction")
            
            substrate = self.setup_context(premises, mode)
            consistency = substrate.evaluate_consistency()
            
            if consistency < 0.5:
                return json.dumps({"error": "Knowledge base is inconsistent."})
                
            chain = self.perform_reasoning(problem, substrate)
            quality = self.assess_quality(chain)
            
            return json.dumps({
                "conclusion": chain.steps[-1].inferred_content if chain.steps else "No conclusion",
                "action": "TREAT" if chain.steps and chain.steps[-1].inferred_content.startswith("TREAT") else
                "WITHHOLD" if chain.steps and chain.steps[-1].inferred_content.startswith("WITHHOLD") else
                "ANSWER",
                "chain_id": chain.chain_id,
                "overall_confidence": chain.overall_confidence,
                "quality_assessment": quality,
                "mode_used": mode,
                "steps": [s.inferred_content for s in chain.steps],
            })
            
        except Exception as e:
            logger.error(f"Reasoning failed: {e}")
            return json.dumps({"error": str(e)})

if __name__ == "__main__":
    agent = H11ReasonAgent("REASON_CORE_01")
    req = json.dumps({
        "problem_statement": "Is Socrates mortal?",
        "premises": ["All men are mortal.", "Socrates is a man."],
        "reasoning_mode": "deduction"
    })
    print(agent.process(req))
