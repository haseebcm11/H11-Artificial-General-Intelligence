import asyncio
from h11_runtime import H11AGI, CaseEnvelope, RiskClass

async def main():
    # 1. Instantiate the Sovereign AGI Kernel (with live Search & Learning)
    agi = H11AGI(enable_search=True, enable_learning=True)
    await agi.initialize()

    # 2. Construct a Case Envelope
    case_payload = {
        "symptoms": ["fever", "chills", "anemia"],
        "travel_history": ["sub-saharan_africa"],
        "suspected_pathogen": "Plasmodium falciparum",
        "patient_vitals": {"temp_c": 39.2, "heart_rate": 110},
        "query": "Evaluate optimal antiparasitic intervention and retrieve latest clinical evidence",
        "goal": "host_infection",
    }

    # 3. Execute the Governed Cognitive Loop (24 Steps)
    result = await agi.tick(case_payload)

    # 4. Inspect Governed Outcome & Live Evidence
    print(f"Case ID: {result.case_id}")
    print(f"Admitted: {result.admitted}")
    print(f"Licensed: {result.licensed}")
    print(f"Retrieved Evidence Count: {len(result.retrieved_evidence)}")
    print(f"Learning Recorded: {result.learning_recorded}")
    print(f"Hops Traversed: {' -> '.join(result.hops)}")
    print(f"Audit Block Hash: {result.audit_head}")

if __name__ == "__main__":
    asyncio.run(main())
