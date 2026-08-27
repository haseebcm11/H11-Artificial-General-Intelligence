import os

dirs = [
    r"d:\My Research\H11 PATENTS\H11-AGI\H11I_INTELLIGENCE_UNIVERSE\D05_life_sciences",
    r"d:\My Research\H11 PATENTS\H11-AGI\H11I_INTELLIGENCE_UNIVERSE\D06_earth_environment",
    r"d:\My Research\H11 PATENTS\H11-AGI\H11I_INTELLIGENCE_UNIVERSE\D07_space_astronomy",
    r"d:\My Research\H11 PATENTS\H11-AGI\H11I_INTELLIGENCE_UNIVERSE\D08_physics",
]

generic_files = []
for d in dirs:
    for root, _, files in os.walk(d):
        for f in files:
            if f == "agent.py":
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                    if "generic placeholder" in content.lower() or "TODO" in content or "Placeholder" in content:
                        generic_files.append(path)
                        
with open("generic_agents.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(generic_files))
print(f"Found {len(generic_files)} generic agents.")
