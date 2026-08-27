"""Deploy H11-AGI to Cloudflare Workers for h11.network."""
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

CF_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "56f03e0e4c2e609d10e2769ffcfa6ac3")
ZONE_ID = os.environ.get("CLOUDFLARE_ZONE_ID", "722db54d698e60a3a36ebdc37cbd311f")
SCRIPT_NAME = "h11-network-agi"

# Load the HTML and template
html_content = Path("h11_runtime/server/static/index.html").read_text(encoding="utf-8")
worker_template = Path("deploy/worker_template.js").read_text(encoding="utf-8")

# Replace placeholder with properly encoded JSON string of the HTML
worker_code = worker_template.replace("HTML_PAGE_PLACEHOLDER", json.dumps(html_content))

boundary = "----CloudflareWorkerBoundary"
metadata = {
    "main_module": "index.js",
    "compatibility_date": "2026-08-01",
    "compatibility_flags": ["nodejs_compat"],
}

body_parts = [
    f"--{boundary}\r\n".encode(),
    b'Content-Disposition: form-data; name="metadata"; filename="blob"\r\n',
    b'Content-Type: application/json\r\n\r\n',
    json.dumps(metadata).encode(),
    b"\r\n",
    f"--{boundary}\r\n".encode(),
    b'Content-Disposition: form-data; name="index.js"; filename="index.js"\r\n',
    b'Content-Type: application/javascript+module\r\n\r\n',
    worker_code.encode("utf-8"),
    b"\r\n",
    f"--{boundary}--\r\n".encode(),
]
body = b"".join(body_parts)

url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{SCRIPT_NAME}"
req = urllib.request.Request(
    url,
    data=body,
    method="PUT",
    headers={
        "Authorization": f"Bearer {CF_TOKEN}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    },
)

try:
    with urllib.request.urlopen(req) as resp:
        res_data = json.loads(resp.read().decode())
        print("Worker script upload success:", res_data.get("success"))
except urllib.error.HTTPError as exc:
    print("Worker upload failed:", exc.code, exc.read().decode())

# Bind routes: h11.network/*, www.h11.network/*, *.h11.network/*
routes_to_bind = ["h11.network/*", "www.h11.network/*", "*.h11.network/*"]
for pattern in routes_to_bind:
    route_url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/workers/routes"
    route_data = json.dumps({"pattern": pattern, "script": SCRIPT_NAME}).encode()
    r_req = urllib.request.Request(
        route_url,
        data=route_data,
        method="POST",
        headers={
            "Authorization": f"Bearer {CF_TOKEN}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(r_req) as resp:
            print(f"Bound route '{pattern}':", json.loads(resp.read().decode()).get("success"))
    except urllib.error.HTTPError as exc:
        err_msg = exc.read().decode()
        if "already exists" in err_msg:
            print(f"Route '{pattern}' already bound.")
        else:
            print(f"Route binding '{pattern}' response:", exc.code, err_msg)
