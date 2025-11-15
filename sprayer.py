import requests
import os
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Validate required environment variables
required_env_vars = ["CATCHERURL", "CATCHERTLS"]
missing_env_vars = [var for var in required_env_vars if os.getenv(var) is None]
if missing_env_vars:
    missing_vars_str = ", ".join(missing_env_vars)
    raise ValueError(f"Missing environment variables: {missing_vars_str}")

# Fetch environment variables
catcher_URL = os.getenv("CATCHERURL")
catcher_uses_TLS = os.getenv("CATCHERTLS").lower() == "true"
instance_id = os.getenv("INSTANCE_ID", "1")

# Configure prox

print(f"[*] Instance ID: {instance_id}")

def send_request():
    """Send a single GET request through the proxy"""
    url = "https://ja4db.com/id/ja4/"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    try:
        print(f"[*] Sending request to {url}")
        response = requests.get(
            url,
            headers=headers,
            proxies = {"http": "http://changeme:changeme@127.0.0.1:1234"},
            verify=False,
            timeout=30,
        )
        
        print(f"[+] Response received: {response.status_code}")
        return response
        
    except requests.RequestException as e:
        print(f"[-] Request failed: {str(e)}")
        return None

def send_data_to_catcher(data):
    """Send data to the catcher via GET request"""
    try:
        print(f"[*] Fetching logs from catcher: {catcher_URL}")
        response = requests.get(
            catcher_URL,
            timeout=10,
            verify=catcher_uses_TLS
        )
        print(f"[+] Catcher response received")
        print(response.text)
        
    except requests.RequestException as e:
        print(f"[-] Failed to fetch from catcher: {str(e)}")

# Send the request
response = send_request()

result = {
    "instance_id": instance_id,
}

if response is not None:
    result["status_code"] = response.status_code
    result["response_body"] = response.text
    result["response_headers"] = dict(response.headers)
    result["url"] = response.url
    result["elapsed_time"] = str(response.elapsed)
    
    # Try to parse JSON if possible
    try:
        result["response_json"] = response.json()
    except:
        result["response_json"] = None
else:
    result["status_code"] = 500
    result["response_body"] = "Request failed"
    result["response_headers"] = {}

# Fetch logs from catcher
print(f"\n[*] Fetching logs from catcher...")
send_data_to_catcher(result)
print("[*] Script completed!")
