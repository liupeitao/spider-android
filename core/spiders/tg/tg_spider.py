
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
import datetime
from pathlib import Path
import time
from typing import Literal
from socks import SOCKS5

import redis
import requests
from lamda.client import GrantType, Point
from config import config
from core.androidspider import AndroidSpider
from core.db.models import App, DeviceModel
from core.db.models import UserModel

from core.tools.ocr import extract_varifycation
from telethon import TelegramClient
redis_client = redis.from_url(config.REDIS_VERIFICATION_URL,  decode_responses=True)





class TGSpider(AndroidSpider):
    def __init__(self, app: App = App(app="Telegram"), device: DeviceModel=DeviceModel(ip=config.LAMDA_HOST, dtype="android")):
        super().__init__(app, device=device)
        self.passwd = ""
        self.password = self.passwd

    def get_varifycation_from_remote(self, countryode, phone):
        # #TODO 从远程获取验证码
        time.sleep(10)
        resp = self.get_develop_signup_code()
        if not  resp['varify']['code']:
            raise Exception("没有提取到验证码")
        print("登录验证码 ", resp['varify']['code'])
        return resp['varify']['code']
    
    def request_varify_code(self) -> str:
        # #TODO 如果发送到邮箱， 否则是短信。。。
        if self.d(textContains="mail").exists() and config.TG_MAIL_LOGIN_SURPORT:
            try:
                res = requests.post(config.SPIDER_WEB_GMAIL_VERIFY_URL, json={
                "app": "Gmail",
                "countrycode": self.countrycode,
                "phone": self.phone,
                "task_uid": "2517d19b-5fea-4aaa-8b2a-d3964e61a1a3"
                })
            except Exception:
                print("没有验证码")
                return
            else:
                verification_code = res.json()[0].split(":")[-1].strip()
                #FIXME  这里是测试代码
                if not verification_code:
                    raise Exception("没有验证码")
                print(f"验证码{verification_code}发送到后台")
                requests.get(f"http://192.168.9.25:8011/add_code?country_code={self.countrycode}&phone_number={self.phone}&code={verification_code}")
                print(f"验证码{verification_code}发送成功")
                return verification_code
                # while True:
                #     verification_code = redis_client.get(f"""{self.app.app}:code:{self.app.countrycode+self.app.phone}""")
                #     if verification_code:
                #         break 
                #     time.sleep(1)
                #     c+=1
                #     if c > 100:
                #         raise Exception("获取验证码超时")
                # return verification_code
        else:
            c =  0
            while True:
                verification_code = redis_client.get(f"""{self.app.app}:code:{self.app.countrycode+self.app.phone}""")
                if verification_code:
                    return verification_code
                time.sleep(1)
                c+=1
                if c > 100:
                    raise Exception("获取验证码超时")
    def scroll_to_bottom(self,reverse=False):
        for i in range(3):
            A = Point(x=300, y=200)
            B = Point(x=300, y=1000)
            if reverse:
                self.d.swipe(A, B)
            self.d.swipe(B, A)
            if f := self.d(resourceId="org.thunderdog.challegram:id/btn_scroll"):
                try:
                    f.click()
                    break
                except Exception:
                    continue


    def crawl_login(self):
        # TODO  触发短信didn't get the code org.thunderdog.challegram:id/btn_forgotPassword
        try:
            tg_client = self.d.application("org.thunderdog.challegram")
            print("===== TgX Login ======")
            print("启动TgX")
            print(
                f"Phone: {self.app.phone} , date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            self.d.start_activity(**{"component": "org.thunderdog.challegram/.MainActivity"})
            print("重置TGx...")
            tg_client.reset_data()
            print("赋予权限， 大约等待10-20s...")
            grant_app(tg_client)
            if self.d(text="Please enter your valid email address.").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)

            elif self.d(textContains="We've sent an SMS with an").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)

            elif self.d(textContains="send an SMS").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)

            elif self.d(textContains="We've sent the code to your email").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)

            elif self.d(textContains="code to the Telegram app on your other").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)
            elif self.d(text="Enter your email address").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)

            elif self.d(textContains="oo many request").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)

            elif self.d(textContains="Invalid").exists():
                print("检测到上次登录失败，重置TgX数据， 大约需要15s")
                tg_client.reset_data()
                grant_app(tg_client)
            time.sleep(1)
            self.d.start_activity(**{"component": "org.thunderdog.challegram/.MainActivity"})
            time.sleep(3)
            if self.d(text="Start Messaging"):
                self.d(text="Start Messaging").click()
            country_code_input = self.d(resourceId="org.thunderdog.challegram:id/login_code")
            time.sleep(2)
            country_code_input.set_text(self.app.countrycode)
            print(f"输入国家代码 {self.app.countrycode}")
            time.sleep(1)

            phone_input = self.d(resourceId="org.thunderdog.challegram:id/login_phone")
            time.sleep(2)
            phone_input.set_text(self.app.phone)
            print(f"输入手机号 {self.app.phone}")
            ack = self.d(resourceId="org.thunderdog.challegram:id/btn_done")
            ack.click()
            time.sleep(6)
            code_input = self.d(className="android.widget.EditText")
            time.sleep(2)
            if not self.d(textContains="sent").exists():
                ret_text = ""
                if self.d(textContains="oo").exists():
                    ret_text = self.d(textContains="oo many request").get_text()
                elif self.d(textContains="Invalid").exists():
                    ret_text = self.d(textContains="Invalid").get_text()
                elif self.d(textContains="to").exists():
                    ret_text = self.d(textContains="to").get_text()
                elif self.d(textContains="your").exists():
                    ret_text = self.d(textContains="your").get_text()
                raise Exception(f"失败。 检测到不是输入验证码页面{ret_text}")
            print("等待20s")
            for i in range(1,20):
                print(i, end=' ')
            code = self.request_varify_code()
            if not code_input.exists():
                raise Exception("没有找到验证码输入框")
            code_input.set_text(code)
            print(f"输入的验证码 {code}")
            time.sleep(2)
            if self.d(textContains="Invalid code").exists():
                print("验证码错误")
                raise Exception("验证码错误")
            else:
                self.d(text="ALLOW").click()
            print("登录成功")
        except Exception as e:
            #TODO 异常: UiSelector[TEXT=Start Messaging] 后续处理
            raise Exception(f"登录失败 {str(e)}")
        else:
            return True

    def get_develop_signup_code(self):
        def open_tg_chat(phone="42777"):
            self.d.start_activity(action="android.intent.action.VIEW", data=f"https://t.me/+{phone}")
            time.sleep(2)
            self.d.click(Point(x=690, y=448))        
        def get_last_varifycation_shot(img_dir: Path)-> list[Path]:
            pathes = []
            ff = self.d(className="android.view.View")
            eles = [
                x
                for x in ff.info_of_all_instances()
                if x.visibleBounds.left == 0
                and x.visibleBounds.right == 720
                and x.visibleBounds.bottom - x.visibleBounds.top > 300
                and x.visibleBounds.bottom - x.visibleBounds.top < 1000
            ]         
            for index, ele in enumerate(eles):
                img_path = img_dir / f"{str(index)}.png"
                self.d.screenshot(quality=60, bound=ele.bounds).save(img_path) 
                pathes.append(img_path) 
            return pathes
        try:
            open_tg_chat()
            self.scroll_to_bottom()
            pathes = get_last_varifycation_shot(img_dir=Path("/home/liupeitao/projects/spider-android/static"))
            ress = []
            for  path in  pathes:
                res = extract_varifycation(path)
                if res['varify']['code'] or res['web_varify']['code']:
                    ress.append(res)
                    print(res['varify']['code'], res['web_varify']['code'])
            return ress[-1]
        except Exception as e:
            print(f"失败没有登录{str(e)}")
            return {}
    
    async def login(self, user:UserModel):
        self.proxy_host = user.config.proxy_host
        self.proxy_port = user.config.proxy_port
        proxy = (SOCKS5, self.proxy_host, self.proxy_port)
        real_phone = self.countrycode + self.phone
        self.api_id = user.api_id
        self.api_hash = user.api_hash
        session_str = str(config.TG_USER_SESSION_DIR / real_phone)
        client = TelegramClient(session_str , self.api_id, self.api_hash, proxy=proxy) 
        try:
            if self.password == "no" or self.password == "":
                await client.start(real_phone,  code_callback=lambda: self.get_varifycation_from_remote(self.countrycode, self.phone)) 
                await client.disconnect()
            else:
                await client.start(real_phone,  password=self.password, code_callback=lambda: self.get_varifycation_from_remote(self.countrycode, self.phone))
                await client.disconnect()
        except Exception as e:
            raise Exception(f"登录失败 {str(e)}")
        else:
            print("登录成功")
            return True
  

    def check_session(self):
        session_path = config.TG_USER_SESSION_DIR  / (self.countrycode + self.phone)
        if not session_path.exists():
            api_id, api_hash = self.check_dev()
            self.api_id = api_id
            self.api_hash = api_hash
            if not api_id or api_hash:
                return None
            self.login(api_id, api_hash)

    def check_dev(self):
        return "", ""
    def crawl(self, witch_task:  Literal['dialogs', 'chats', 'members']):
        if witch_task == "dialogs":
            self.crawl_dialogs()
        elif witch_task == "chats":
            self.crawl_chats()
        elif witch_task == "members":
            self.crawl_members()
        else:
            print("没有这个任务")
        

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
