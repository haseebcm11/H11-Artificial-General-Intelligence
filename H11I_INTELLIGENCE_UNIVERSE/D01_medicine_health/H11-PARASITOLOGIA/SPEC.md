> **Layer 1** · Medicine & Health Sciences · `H11-PARASITOLOGIA`

## Purpose
H11-PARASITOLOGIA models the complex, multi-stage lifecycles of protozoan and helminthic parasites (e.g., Plasmodium, Schistosoma, Ascaris). Unlike bacteria or viruses, parasites often require multiple hosts (vectors) and undergo drastic morphological changes across different organs within the human host, making their pathogenesis deeply systemic.

## Technical Deep-Dive
The agent utilizes a distributed state-machine representing the lifecycle stages of parasites (e.g., sporozoite -> merozoite -> trophozoite -> gametocyte). Movement between states is tied to spatial migration through the ANATOMIA graph (e.g., skin -> liver -> bloodstream).

For helminths, the agent tracks macro-parasite burden (worm count) rather than micro-parasite density. It simulates physical obstruction (e.g., lymphatic filariasis, biliary obstruction) and competition for host nutrients. Eosinophilic immune evasion mechanisms are mathematically modeled to resist IMMUNOLOGIA's standard clearance rates.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| parasite_species | ParasiteData | Specifies lifecycle stages and tropism. |
| vector_exposure | VectorEvent | Bite from mosquito, sandfly, or ingestion. |
| host_anatomy | AnatomyGraph | Required for migration routing. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| parasitic_burden | Int/Float | Worm count or parasitemia percentage. |
| lifecycle_stage | StageEnum | Current predominant form in the host. |
| systemic_effects | List[Effect] | Anemia, eosinophilia, organ obstruction. |

### State Schema
Maintains `HostParasiteState` detailing the distribution of different lifecycle forms across various anatomical compartments.

## Dependencies
### Upstream (depends on)
H11-ANATOMIA (migration paths), H11-EPIDEMIOLOGIA (vector dynamics)
### Downstream (feeds into)
H11-PHYSIOLOGIA (nutrient drain, anemia), H11-PATHOLOGIA

## Failure Modes
1. Migration Dead-ends: Parasite gets stuck in an anatomical compartment due to graph topology errors.
2. Lifecycle Desync: Missing a trigger (like RBC rupture) causing the parasite to freeze in one stage forever.
3. Micro/Macro Confusion: Applying bacterial logistic growth to adult worms, resulting in millions of meter-long tapeworms.

## Performance Characteristics
State transitions are event-driven rather than continuous. Pathfinding algorithms for tissue migration can cause minor latency spikes upon initial infection.

## Research References
- Manson's Tropical Diseases.
- Mathematical models of malaria transmission and within-host dynamics.

## Implementation Notes
Heavily utilizes event queues to manage the delayed transitions between life stages (e.g., the 7-10 day hepatic phase of Plasmodium before blood stage).
