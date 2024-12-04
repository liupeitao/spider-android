"""
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-11-25 20:19:13
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-11-27 09:56:48
FilePath: /lamda/android/tg/tgx.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

"""
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-11-25 20:19:13
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-11-26 15:16:15
FilePath: /lamda/android/tg/tgx.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

# intent.setAction("android.intent.action.VIEW");
# intent.setData(android.net.Uri.parse("tg://resolve?phone=" + phoneNumber));
import pickle
import time
from pathlib import Path

import redis
import datetime
import requests
from lamda.client import Device, GrantType, Point
from lamda.const import *

from core.db.models import App
from core.tools.ocr import extract_varifycation

from core.spider import Spider

redis_client = redis.from_url("redis://:root123456@192.168.9.37:6379/0",  decode_responses=True)


def get_varifycation_from_remote():
    return requests.get(
        "http://192.168.9.25:8011/code", params={"phone_number": "18112953195"}
    )


d = Device("192.168.9.6")


class TGSpider(Spider):
    def __init__(self, app: App = App(app="Telegram"), *args, **kwargs):
        super().__init__(app, *args, **kwargs)

    def wait_for_code(self) -> str:
        return redis_client.get(
            f"""{self.app.app}:code:{self.app.countrycode.countrycode+self.app.phone}"""
        )

    def crawl_login(self):
        try:
            tg_client = d.application("org.thunderdog.challegram")
            print("===== TgX Login ======")
            print("启动TgX")
            print(
                f"Phone: {self.app.phone} , date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            d.start_activity(**{"component": "org.thunderdog.challegram/.MainActivity"})
            print("重置TGx...")
            tg_client.reset_data()
            print("赋予权限， 大约等待10-20s...")
            grant_app(tg_client)
            if d(text="Please enter your valid email address.").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)

            elif d(textContains="We've sent an SMS with an").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)

            elif d(textContains="send an SMS").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)

            elif d(textContains="We've sent the code to your email").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)

            elif d(textContains="code to the Telegram app on your other").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)
            elif d(text="Enter your email address").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)

            elif d(textContains="oo many request").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)

            elif d(textContains="Invalid").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)
            time.sleep(1)
            d.start_activity(**{"component": "org.thunderdog.challegram/.MainActivity"})
            time.sleep(3)
            if d(text="Start Messaging"):
                d(text="Start Messaging").click()
            phone_input = d(resourceId="org.thunderdog.challegram:id/login_phone")
            time.sleep(2)
            phone_input.set_text(self.app.phone)
            print(f"输入手机号 {self.app.phone}")
            ack = d(resourceId="org.thunderdog.challegram:id/btn_done")
            ack.click()
            time.sleep(6)
            code_input = d(className="android.widget.EditText")
            time.sleep(2)
            if not d(textContains="sent").exists():
                ret_text = ""
                if d(textContains="oo").exists():
                    ret_text = d(textContains="oo many request").get_text()
                elif d(textContains="Invalid").exists():
                    ret_text = d(textContains="Invalid").get_text()
                elif d(textContains="to").exists():
                    ret_text = d(textContains="to").get_text()
                elif d(textContains="your").exists():
                    ret_text = d(textContains="your").get_text()
                print(f"失败。 检测到不是输入验证码页面 原因:{ret_text}")
                print("即将退出")
                return
            time.sleep(40)
            code = self.wait_for_code()
            if not code_input.exists():
                print("没有输入验证码的窗口")
                return
            code_input.set_text(code)
            print(f"输入验证码 {code}")
            time.sleep(2)
            if d(textContains="Invalid code").exists():
                print("验证码错误")
            else:
                d(text="ALLOW").click()
            print("登录成功")
            return
        except Exception as e:
            print(f"异常: {str(e)}")
        finally:
            return None


def grant_app(app):
    permissions = [
        "android.permission.CAMERA",
        "android.permission.FLASHLIGHT",
        "android.permission.INTERNET",
        "android.permission.READ_CONTACTS",
        "android.permission.POST_NOTIFICATIONS",
    ]
    for permission in permissions:
        try:
            app.grant(permission, mode=GrantType.GRANT_ALLOW)
        except Exception:
            pass


def open_tg_chat(phone="42777"):
    d.start_activity(action="android.intent.action.VIEW", data=f"https://t.me/+{phone}")
    time.sleep(2)
    d.click(Point(x=690, y=448))


def scroll_to_bottom(reverse=False):
    for i in range(3):
        A = Point(x=300, y=200)
        B = Point(x=300, y=1000)
        if reverse:
            d.swipe(A, B)
        d.swipe(B, A)
        if f := d(resourceId="org.thunderdog.challegram:id/btn_scroll"):
            try:
                f.click()
                break
            except Exception:
                continue


def get_last_varifycation(img_path: Path):
    ff = d(className="android.view.View")
    eles = [
        x
        for x in ff.info_of_all_instances()
        if x.visibleBounds.left == 0
        and x.visibleBounds.right == 720
        and x.visibleBounds.bottom - x.visibleBounds.top > 500
        and x.visibleBounds.bottom - x.visibleBounds.top < 1000
    ]
    d.screenshot(quality=60, bound=eles[0].bounds).save(img_path)


def screent_shot_varify(img_path: Path):
    open_tg_chat()
    scroll_to_bottom()
    get_last_varifycation(img_path=img_path)


def get_varifycation(phone, img_path: Path):
    screent_shot_varify(img_path=img_path)
    res = extract_varifycation(img_path)
    redis_client.setex(phone, 60, value=pickle.dumps(res))
    res.pop("img")
    print(res)
    return res