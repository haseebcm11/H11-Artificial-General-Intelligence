"""Embed base64 logo directly into index.html and update worker_template.js."""
from pathlib import Path

b64_raw = Path("h11_runtime/server/static/logo_b64.txt").read_text().strip()
# b64_raw starts with "data:image/jpeg;base64,..."
b64_pure = b64_raw.split(",", 1)[1] if "," in b64_raw else b64_raw

# 1. Update index.html
html_path = Path("h11_runtime/server/static/index.html")
html = html_path.read_text(encoding="utf-8")

# Replace any /logo.jpg with the inline base64 data URI
html = html.replace('src="/logo.jpg"', f'src="{b64_raw}"')
html_path.write_text(html, encoding="utf-8")
print("index.html updated with direct base64 image data URI!")

# 2. Update deploy/worker_template.js to handle /logo.jpg requests as binary image
worker_js_path = Path("deploy/worker_template.js")
worker_js = worker_js_path.read_text(encoding="utf-8")

logo_route_code = f'''
    if (url.pathname === "/logo.jpg" || url.pathname === "/assets/logo.jpg") {{
      const b64 = "{b64_pure}";
      const binaryString = atob(b64);
      const bytes = new Uint8Array(binaryString.length);
      for (let i = 0; i < binaryString.length; i++) {{
        bytes[i] = binaryString.charCodeAt(i);
      }}
      return new Response(bytes, {{
        headers: {{
          "Content-Type": "image/jpeg",
          "Cache-Control": "public, max-age=86400"
        }}
      }});
    }}
'''

if 'url.pathname === "/logo.jpg"' not in worker_js:
    # Insert right after `const url = new URL(request.url);`
    target = "const url = new URL(request.url);"
    worker_js = worker_js.replace(target, target + "\n" + logo_route_code)
    worker_js_path.write_text(worker_js, encoding="utf-8")
    print("deploy/worker_template.js updated with /logo.jpg binary handler!")
