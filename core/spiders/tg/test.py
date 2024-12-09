import requests
def requests_varify_code(phone, countrycode):
    resp = requests.post(
        "http://192.168.9.31:7002/api/v1/Task/Telegram/varification",
        json={
            "app": "Amap",
            "countrycode": countrycode,
            "phone": phone,
            "task_uid": "2517d19b-5fea-4aaa-8b2a-d3964e61a1a3",
        },
    )
    print(resp.json()['web_varify']['code'])
    return resp.json()['web_varify']['code']


w = requests_varify_code("13349150214", "86")
print(w)
