import requests

tests = [
    "http://localhost:8000/channel/overview",
    "http://localhost:8000/channel/affiliates",
    "http://localhost:8000/channel/compare",
    "http://localhost:8000/shop-summary/list",
    "http://localhost:8000/dashboard/gmvmax-overview",
    "http://localhost:8000/gmvmax/campaigns?advertiser_id=7615246831711862800",
    "http://localhost:8000/rules",
    "http://localhost:8000/creatives",
]

for url in tests:
    try:
        r = requests.get(url, timeout=5)
        path = url.replace("http://localhost:8000", "")
        status = "OK" if r.status_code == 200 else "FAIL"
        print(f"[{status}] {r.status_code}  {path}")
    except Exception as e:
        print(f"[ERR]  {url.replace('http://localhost:8000','')}: {e}")
