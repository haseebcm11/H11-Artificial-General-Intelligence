"""Run one H11 tick from the command line.

Examples:
  python -m h11_runtime --patient P-1001 --travel Kenya --symptoms fever,chills --smear 5200
  python -m h11_runtime --query "Is Socrates mortal?" --premise "All men are mortal." --premise "Socrates is a man."
  python -m h11_runtime --patient P-1001 --query "what parasite was identified?"
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys

from .agi import H11AGI


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="h11_runtime", description="Run one H11 cognitive tick.")
    p.add_argument("--patient", dest="patient_id", help="Patient or identity id")
    p.add_argument("--travel", default="", help="Comma-separated travel history")
    p.add_argument("--symptoms", default="", help="Comma-separated symptoms")
    p.add_argument("--smear", type=float, default=None, help="Blood smear density per uL")
    p.add_argument("--query", default="", help="Free-form question")
    p.add_argument("--premise", action="append", default=[], help="Premise for the reasoner (repeatable)")
    p.add_argument("--json", action="store_true", help="Print the full result payload as JSON")
    return p.parse_args(argv)


async def run(ns: argparse.Namespace) -> int:
    case: dict = {}
    if ns.patient_id:
        case["patient_id"] = ns.patient_id
    if ns.travel:
        case["travel_history"] = [x.strip() for x in ns.travel.split(",") if x.strip()]
    if ns.symptoms:
        case["symptoms"] = [x.strip() for x in ns.symptoms.split(",") if x.strip()]
    if ns.smear is not None:
        case["blood_smear_density_per_ul"] = ns.smear
    if ns.query:
        case["query"] = ns.query
    if ns.premise:
        case["premises"] = list(ns.premise)
    if not case:
        print("Provide a medical case (--symptoms/--smear) or a --query.", file=sys.stderr)
        return 2

    agi = H11AGI()
    result = await agi.tick(case)
    if ns.json:
        print(
            json.dumps(
                {
                    "case_id": result.case_id,
                    "admitted": result.admitted,
                    "domain": result.domain,
                    "pipeline_id": result.pipeline_id,
                    "action": result.action,
                    "allowed": result.allowed,
                    "licensed": result.licensed,
                    "halted": result.halted,
                    "hops": result.hops,
                    "conclusion": (result.payload.get("reason") or {}).get("conclusion"),
                    "diagnosis": result.payload.get("diagnosis"),
                    "alignment": result.payload.get("alignment"),
                    "error": result.error,
                },
                indent=2,
            )
        )
        return 0 if result.admitted and not result.error else 1

    print(f"admitted={result.admitted} domain={result.domain} pipeline={result.pipeline_id}")
    print(f"action={result.action or '-'} allowed={result.allowed} licensed={result.licensed} halted={result.halted}")
    if result.payload.get("diagnosis"):
        dx = result.payload["diagnosis"]
        print(f"diagnosis={dx.get('identified_parasite')} drug={dx.get('recommended_antiparasitic')}")
    conclusion = (result.payload.get("reason") or {}).get("conclusion")
    if conclusion:
        print(f"conclusion={conclusion}")
    if result.error:
        print(f"error={result.error}", file=sys.stderr)
        return 1
    return 0


def main() -> None:
    raise SystemExit(asyncio.run(run(parse_args(sys.argv[1:]))))


if __name__ == "__main__":
    main()
