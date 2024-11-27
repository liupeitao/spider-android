"""
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-11-26 17:43:56
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-11-27 13:40:12
FilePath: /spider-android/android/douyin/douyin.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

import time

from lamda.client import Device


class App:
    app = ""


d = Device("192.168.9.47")
headers = {
    # "x-nonce": "5fde936e-9464-438c-981d-5f007226acc6",
    "os_ver": "33",
    "device_model": "android",
    "x-timestamp": f"{time.time()}",
    "Connection": "Keep-Alive",
    "language": "zhs",
    "auth_ver": "2.11.56",
    # "If-None-Match": 'W/"7b-GNGKzcVHXS9xKqxs+qiNOQeShbE"',
    "Authorization": "Bearer M0Z5MTNZZ1NYcG1IdFZVa0xBYmpQZFlhU2hXa1loT20=",
    "client_ver": "2.11.56",
    "x-username": "t215030949",
    "x-signature": "281f6e28afc64ba1b9d4a0c0e3a9afb849c2dc5d90c4f5aab3e5baed51a5d2c7",
    "device": "android",
    "Content-Type": "application/json",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; ME61 Build/TKQ1.230331.002)",
    "Host": "prdelb.hotcoffeefactory.net",
    "Accept-Encoding": "gzip",
}
# r = requests.get(
#     "https://prdelb.hotcoffeefactory.net/api/v4/contact/search/?type=phone&key=8613349150214&captchaId=&captchaCode=",
# )


# headers = {
#     # "x-nonce": "5fde936e-9464-438c-981d-5f007226acc6",
#     "os_ver": "33",
#     "device_model": "android",
#     "x-timestamp": f"{time.time()}",
#     "Connection": "Keep-Alive",
#     "language": "zhs",
#     "auth_ver": "2.11.56",
#     # "If-None-Match": 'W/"7b-GNGKzcVHXS9xKqxs+qiNOQeShbE"',
#     "Authorization": "Bearer M0Z5MTNZZ1NYcG1IdFZVa0xBYmpQZFlhU2hXa1loT20=",
#     "client_ver": "2.11.56",
#     "x-username": "t215030949",
#     "x-signature": "281f6e28afc64ba1b9d4a0c0e3a9afb849c2dc5d90c4f5aab3e5baed51a5d2c7",
#     "device": "android",
#     "Content-Type": "application/json",
#     "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; ME61 Build/TKQ1.230331.002)",
#     "Host": "prdelb.hotcoffeefactory.net",
#     "Accept-Encoding": "gzip",
# }
# r = requests.get(
#     "https://prdelb.hotcoffeefactory.net/api/v4/contact/search/?type=phone&key=8613349150214&captchaId=&captchaCode=",
#     headers=headers,
# )


w = d(className="android.widget.TextView")
c = w.info_of_all_instances()
for i in c:
    print(c.text)
