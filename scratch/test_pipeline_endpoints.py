import urllib.request
import urllib.error
import json
import os

LOG_FILE = "C:/Users/ASUS/.gemini/antigravity/brain/b39c6150-d74a-411e-abcf-bb7e90dfcf32/scratch/ui_test_log.txt"

def run_test():
    results = []
    results.append("=== STARTING LIVE ENDPOINT TESTING ===")
    
    # 1. Test frontend server
    try:
        resp = urllib.request.urlopen("http://127.0.0.1:3000", timeout=5)
        results.append(f"[PASS] Frontend server is serving page: HTTP {resp.status}")
    except Exception as e:
        results.append(f"[FAIL] Frontend server failed: {e}")

    # 2. Test backend server root/docs
    try:
        resp = urllib.request.urlopen("http://127.0.0.1:8000/docs", timeout=5)
        results.append(f"[PASS] Backend server is serving OpenAPI docs: HTTP {resp.status}")
    except Exception as e:
        results.append(f"[FAIL] Backend server failed: {e}")

    # 3. Test invalid login returns 401
    url = "http://127.0.0.1:8000/api/auth/login"
    data = json.dumps({"email": "test@test.com", "password": "wrongpassword"}).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        results.append(f"[FAIL] Login with invalid credentials returned HTTP {resp.status} (expected 401)")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            results.append("[PASS] Login with invalid credentials correctly returned HTTP 401 Unauthorized")
        else:
            results.append(f"[FAIL] Login with invalid credentials returned unexpected HTTP {e.code}")
    except Exception as e:
        results.append(f"[FAIL] Login endpoint error: {e}")

    # Write log results
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    
    print("\n".join(results))

if __name__ == "__main__":
    run_test()
