import os
import json
import urllib.request
from io import BytesIO

ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "56f03e0e4c2e609d10e2769ffcfa6ac3")
SCRIPT_NAME = "h11-agi"
ZONE_ID = os.environ.get("CLOUDFLARE_ZONE_ID", "722db54d698e60a3a36ebdc37cbd311f")
API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")

def deploy():
    if not API_TOKEN:
        raise ValueError("CLOUDFLARE_API_TOKEN environment variable must be set.")

    with open("deploy/worker_template.js", "r", encoding="utf-8") as f:
        worker_code = f.read()

    # Build multipart form data for Cloudflare ES module worker
    boundary = "----WebKitFormBoundaryH11WorkerBoundary7MA4YWxkTrZu0gW"
    body = BytesIO()
    
    # 1. metadata part
    metadata = json.dumps({"main_module": "worker.js", "compatibility_date": "2024-04-01"}).encode("utf-8")
    body.write(f"--{boundary}\r\n".encode("utf-8"))
    body.write(b'Content-Disposition: form-data; name="metadata"\r\n')
    body.write(b'Content-Type: application/json\r\n\r\n')
    body.write(metadata)
    body.write(b"\r\n")

    # 2. worker script part
    body.write(f"--{boundary}\r\n".encode("utf-8"))
    body.write(b'Content-Disposition: form-data; name="worker.js"; filename="worker.js"\r\n')
    body.write(b'Content-Type: application/javascript+module\r\n\r\n')
    body.write(worker_code.encode("utf-8"))
    body.write(b"\r\n")
    body.write(f"--{boundary}--\r\n".encode("utf-8"))

    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{SCRIPT_NAME}"
    req = urllib.request.Request(
        url,
        data=body.getvalue(),
        headers={
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="PUT",
    )
    with urllib.request.urlopen(req) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
        print(f"Worker script upload success: {res_data.get('success')}")

    # Ensure Routes
    routes = ["h11.network/*", "www.h11.network/*", "*.h11.network/*"]
    for pattern in routes:
        route_url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/workers/routes"
        payload = json.dumps({"pattern": pattern, "script": SCRIPT_NAME}).encode("utf-8")
        req = urllib.request.Request(
            route_url,
            data=payload,
            headers={
                "Authorization": f"Bearer {API_TOKEN}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req) as resp:
                print(f"Route '{pattern}' created successfully.")
        except urllib.error.HTTPError as e:
            err_data = json.loads(e.read().decode("utf-8"))
            msg = err_data.get("errors", [{}])[0].get("message", "")
            if "already exists" in msg or "already bound" in msg or "duplicate" in msg.lower():
                print(f"Route '{pattern}' already bound.")
            else:
                print(f"Route error for '{pattern}': {msg}")

if __name__ == "__main__":
    deploy()
