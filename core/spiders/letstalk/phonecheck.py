import requests

import time
headers = {
# "x-nonce": "4308a4b0-6dda-4858-b990-9b16300d8b13",
"os_ver": "33",
"device_model": "android",
"x-timestamp": "1730877552628",
"Connection": "Keep-Alive",
"language": "zhs",
"auth_ver": "2.11.56",
"Authorization": "Bearer YXo2RHhhT04xR0VDQnBWd29CYUJ4aHVnWWZMRzRxTktYZkUza1lLbW5sQjFPZk5WSjcwUEs1cmRiamNnczJGMA==",
"client_ver": "2.11.56",
"x-username": "t215030949",
"x-signature": "9601b9fa56c3c3ceebe2e0bfaae7d56b4dffc562c3c03da8b726e76506852df9",
"device": "android",
"Content-Type": "application/json",
"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; ME61 Build/TKQ1.230331.002)",
"Host": "prdapi.btcric33.com",
"Accept-Encoding": "gzip"
}


phones = ["8613349150214"]

for phone in phones:
    r = requests.get(
        f"https://prdapi.btcric33.com/api/v4/contact/search/?type=phone&key=+{phone}&captchaId=&captchaCode=",
        headers=headers,
    )
    print({phone: r.text})
