import requests

adv = "7615246831711862800"
for ep in ["overview", "affiliates", "compare"]:
    r = requests.get(f"http://localhost:8000/channel/{ep}?advertiser_id={adv}")
    status = "OK" if r.status_code == 200 else "FAIL"
    print(f"[{status}] /channel/{ep}  {str(r.json())[:100]}")
