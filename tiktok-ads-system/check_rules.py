import requests, json

r = requests.get('http://localhost:8000/rules')
data = r.json()
print(f"规则总数: {data['total']}")
for rule in data['rules']:
    status = "ON " if rule['is_enabled'] else "OFF"
    print(f"  [{status}] [{rule['severity']:8}] {rule['rule_key']:30} {rule['rule_name']}")
    print(f"            params: {json.dumps(rule['params'], ensure_ascii=False)}")
