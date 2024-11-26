import requests
headers = {"x-nonce":"a00c358b-b353-470e-81bd-b9b834b36eae","os_ver":"33","device_model":"android","x-timestamp":"1729215231217","Connection":"Keep-Alive","language":"zhs","auth_ver":"2.11.56","Authorization":"Bearer M0Z5MTNZZ1NYcG1IdFZVa0xBYmpQZFlhU2hXa1loT20=","client_ver":"2.11.56","x-username":"t215030949","x-signature":"b18ee544c915a02663f4bbc3a1a4e6948d97cbc0ee5ee8e2fe5bdd01f0b24a8d","device":"android","Content-Type":"application/json","User-Agent":"Dalvik/2.1.0 (Linux; U; Android 13; ME61 Build/TKQ1.230331.002)","Host":"prdelb.hotcoffeefactory.net","Accept-Encoding":"gzip"}
r = requests.get("https://prdelb.hotcoffeefactory.net/message/schedule/t215030949?time=1729215231212&offset=8&topic=user/t578496174/MessageBox&after=1", headers=headers)
print(r.text)
