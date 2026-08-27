"""Embed official H11-AGI logo into web interface and README.md."""
from pathlib import Path

logo_b64 = Path("h11_runtime/server/static/logo_b64.txt").read_text().strip()
html_file = Path("h11_runtime/server/static/index.html")
html = html_file.read_text(encoding="utf-8")

# Add favicon if not already present
if "rel=\"icon\"" not in html:
    favicon_tag = f'<link rel="icon" type="image/jpeg" href="{logo_b64}">'
    html = html.replace("<!-- Modern Minimalist Typography -->", f"{favicon_tag}\n    <!-- Modern Minimalist Typography -->")

# Update header logo
old_header_logo = """<div class="w-6 h-6 rounded bg-white text-black font-mono font-bold text-xs flex items-center justify-center">
                H
            </div>"""
new_header_logo = f'<img src="{logo_b64}" alt="H11" class="w-7 h-7 rounded-lg object-cover border border-white/10 shadow-sm">'
if old_header_logo in html:
    html = html.replace(old_header_logo, new_header_logo)

# Update hero cover logo
old_hero_emblem = """<!-- Sovereign Emblem -->
        <div class="space-y-4">
            <div class="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full border border-white/[0.1] bg-zinc-950/80 text-[11px] font-mono text-zinc-400">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                <span>H11-AGI • Sovereign Cognitive Operating System</span>
            </div>"""

new_hero_emblem = f"""<!-- Sovereign Emblem -->
        <div class="space-y-6">
            <div class="relative inline-block">
                <div class="w-32 h-32 md:w-40 md:h-40 rounded-3xl p-1 bg-gradient-to-tr from-cyan-400/30 via-amber-400/30 to-blue-500/30 border border-white/10 shadow-2xl shadow-cyan-500/20">
                    <img src="{logo_b64}" alt="H11-AGI Sovereign Logo" class="w-full h-full rounded-[22px] object-cover">
                </div>
            </div>

            <div class="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full border border-white/[0.1] bg-zinc-950/80 text-[11px] font-mono text-zinc-400">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                <span>H11-AGI • Sovereign Cognitive Operating System</span>
            </div>"""

if old_hero_emblem in html:
    html = html.replace(old_hero_emblem, new_hero_emblem)

html_file.write_text(html, encoding="utf-8")
print("Successfully embedded official logo into index.html!")
