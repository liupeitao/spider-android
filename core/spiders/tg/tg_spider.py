
"""
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-11-25 20:19:13
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-11-26 15:16:15
FilePath: /lamda/android/tg/tgx.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

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
from core.db.models import App, DeviceModel, StateEnum
from core.db.models import UserModel

from core.tools.deco import deco_log_state
from core.tools.ocr import extract_varifycation
from telethon import TelegramClient
redis_client = redis.from_url(config.REDIS_VERIFICATION_URL,  decode_responses=True)


class TGSpider(AndroidSpider):
    def __init__(self, app: App = App(app="Telegram"), device: DeviceModel=DeviceModel(ip=config.LAMDA_HOST, dtype="android")):
        super().__init__(app, device=device)
        self.passwd = ""
        self.password = self.passwd

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

    def get_varifycation_from_remote(self, countryode, phone):
        # #TODO 从远程获取验证码
        time.sleep(10)
        resp = self.crawl_dev()
        if not  resp['varify']['code']:
            raise Exception("没有提取到验证码")
        print("登录验证码 ", resp['varify']['code'])
        return resp['varify']['code']
    def send_verification(self, verification_code):
        requests.get(f"http://192.168.9.25:8011/add_code?country_code={self.countrycode}&phone_number={self.phone}&code={verification_code}")
    
    def send_info(self, info):
        requests.get(f"http://localhost:7002/api/v1/Task/Telegram/logintip?country_code={self.countrycode}&phone_number={self.phone}&code={info}")
    
    
    # 用于登录
    # @deco_log_state(state=StateEnum.STARTING)
    def crawl_login_code(self,  ) -> str:
        # #TODO 如果发送到邮箱， 否则是短信。。。
        # if self.d(textContains="mail").exists() and config.TG_MAIL_LOGIN_SURPORT:
        # 从gmail获取验证码， 然后发送到后台， 然后从redis中获取验证码, 这里不应该要影响后续的逻辑
        def send_verify():
            try:
                res = requests.post(config.SPIDER_WEB_GMAIL_VERIFY_URL, json={
                "app": "Gmail",
                "countrycode": self.countrycode,
                "phone": self.phone,
                "task_uid": str(self.app.task_uid)
                })
                verification_code = res.json()[0].split(":")[-1].strip()
                #FIXME  这里是测试代码
                if not verification_code:
                    return
                print(f"验证码{verification_code}发送到后台")
                #FIXME  这里的路径
                self.send_verification(verification_code)
                print(f"验证码{verification_code}发送成功")
            except Exception:
                print("没有验证码")
                return
        
        def acquire_code():
            c = 0
            while True:
                verification_code = redis_client.get(f"""{self.app.app}:code:{self.app.countrycode+self.app.phone}""")
                if verification_code:
                    return verification_code
                time.sleep(1)
                c+=1
                if c > 100:
                    raise Exception("没有获取到验证码")
        send_verify()
        return acquire_code()
    
    #用于 dev帐号和session
    @deco_log_state(state=StateEnum.STARTING)
    def crawl_verify(self):
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
            pathes = get_last_varifycation_shot(img_dir=config.IMG_DIR)
            ress = []
            for  path in  pathes:
                res = extract_varifycation(path)
                if res['varify']['code'] or res['web_varify']['code']:
                    ress.append(res)
                    print(res['varify']['code'], res['web_varify']['code'])
            return ress[-1]
        except Exception as e:
            raise Exception(f"提取验证码失败: {str(e)}")

    # -获取会话
    @deco_log_state(state=StateEnum.STARTING)
    async def crawl_session(self, user:UserModel):
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
    
    def have_second_vrify(self) -> str | bool: 
        if self.d(textContains="is proteccted").exists():
            return self.d(textContains="is proteccted").get_text()
        return False

    def check_mail(self) -> str|bool:
        if self.d(textContains="mail").exists():
            return self.d(textContains="mail").get_text()
        return False

    @deco_log_state(state=StateEnum.STARTING)
    def crawl_login(self):
        if config.TG_MAIL_LOGIN_SURPORT:
            try:
                requests.post(config.SPIDER_WEB_LOGIN_PAGE, json=[{
                    "app": "Telegram",
                    "countrycode": self.countrycode,
                    "phone": self.phone,
                    "task_uid": str(self.app.task_uid)
                }])
            except Exception as e:
                raise Exception(f"浏览器打开失败 {str(e)}")
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
            check_mail = self.check_mail()
            if isinstance(check_mail, str):
                self.send_info(check_mail)
                raise Exception(f"需要邮箱验证, 请重试{check_mail}")
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
                raise Exception(f"=>{ret_text}")
            print("等待20s")
            for i in range(1,10):
                print(i, end=' ')
            code = self.crawl_login_code()
            if not code_input.exists():
                raise Exception("没有找到验证码输入框")
            code_input.set_text(code)
            print(f"输入的验证码 {code}")
            time.sleep(2)
            if self.d(textContains="Invalid code").exists():
                print("验证码错误")
                raise Exception("验证码错误")
            have_second_vrify = self.have_second_vrify()
            if isinstance(have_second_vrify, str):
                print(have_second_vrify)
                self.send_info(have_second_vrify)
                raise Exception("需要二次验证。 填写密码后重试")
            self.d(text="ALLOW").click()
            print("登录成功")
        except Exception as e:
            #TODO 异常: UiSelector[TEXT=Start Messaging] 后续处理
            raise Exception(f"登录失败 {str(e)}")
        
        else:
            return True


    def check_session(self):
        session_path = config.TG_USER_SESSION_DIR  / (self.countrycode + self.phone)
        if not session_path.exists():
            api_id, api_hash = self.check_dev()
            self.api_id = api_id
            self.api_hash = api_hash
            if not api_id or api_hash:
                return None
            self.crawl_session(api_id, api_hash)

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
