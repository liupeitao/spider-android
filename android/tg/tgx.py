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
from lamda.client import Device, GrantType, Point
from lamda.const import *

from tools.ocr import extract_varifycation

redis_client = redis.from_url("redis://:root123456@192.168.9.37:6379/0")


def get_varifycation_from_remote():
    return "34234"


d = Device("192.168.9.6")


# 授予 READ_PHONE_STATE 权限
def grant_app(app):
    try:
        app.grant("android.permission.CAMERA", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.FLASHLIGHT", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.INTERNET", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.ACCESS_NETWORK_STATE", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.ACCESS_FINE_LOCATION", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant(
            "android.permission.ACCESS_COARSE_LOCATION", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant(
            "android.permission.ACCESS_BACKGROUND_LOCATION", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant(
            "android.permission.READ_EXTERNAL_STORAGE", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant(
            "android.permission.WRITE_EXTERNAL_STORAGE", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant("android.permission.RECORD_AUDIO", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant(
            "android.permission.MODIFY_AUDIO_SETTINGS", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant("android.permission.WAKE_LOCK", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.VIBRATE", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.READ_CONTACTS", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.USE_FINGERPRINT", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.FOREGROUND_SERVICE", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant(
            "android.permission.FOREGROUND_SERVICE_LOCATION", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant(
            "android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK",
            mode=GrantType.GRANT_ALLOW,
        )
    except Exception:
        pass

    try:
        app.grant(
            "android.permission.FOREGROUND_SERVICE_PHONE_CALL",
            mode=GrantType.GRANT_ALLOW,
        )
    except Exception:
        pass

    try:
        app.grant("android.permission.MANAGE_OWN_CALLS", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.CHANGE_CONFIGURATION", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.READ_PHONE_STATE", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant(
            "android.permission.RECEIVE_BOOT_COMPLETED", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant("android.permission.SYSTEM_ALERT_WINDOW", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.WRITE_SETTINGS", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.BLUETOOTH", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant(
            "android.permission.REQUEST_INSTALL_PACKAGES", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant("android.permission.POST_NOTIFICATIONS", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.READ_MEDIA_IMAGES", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.READ_MEDIA_VIDEO", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.READ_MEDIA_AUDIO", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant(
            "com.google.android.providers.gsf.permission.READ_GSERVICES",
            mode=GrantType.GRANT_ALLOW,
        )
    except Exception:
        pass

    try:
        app.grant(
            "com.google.android.c2dm.permission.RECEIVE", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant(
            "org.thunderdog.challegram.permission.MAPS_RECEIVE",
            mode=GrantType.GRANT_ALLOW,
        )
    except Exception:
        pass

    try:
        app.grant(
            "org.thunderdog.challegram.permission.C2D_MESSAGE",
            mode=GrantType.GRANT_ALLOW,
        )
    except Exception:
        pass

    try:
        app.grant(
            "com.sec.android.provider.badge.permission.READ", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant(
            "com.sec.android.provider.badge.permission.WRITE",
            mode=GrantType.GRANT_ALLOW,
        )
    except Exception:
        pass

    try:
        app.grant(
            "com.htc.launcher.permission.READ_SETTINGS", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant(
            "com.htc.launcher.permission.UPDATE_SHORTCUT", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant(
            "com.sonyericsson.home.permission.BROADCAST_BADGE",
            mode=GrantType.GRANT_ALLOW,
        )
    except Exception:
        pass

    try:
        app.grant(
            "com.sonymobile.home.permission.PROVIDER_INSERT_BADGE",
            mode=GrantType.GRANT_ALLOW,
        )
    except Exception:
        pass

    try:
        app.grant(
            "com.anddoes.launcher.permission.UPDATE_COUNT", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant(
            "com.majeur.launcher.permission.UPDATE_BADGE", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant(
            "com.huawei.android.launcher.permission.CHANGE_BADGE",
            mode=GrantType.GRANT_ALLOW,
        )
    except Exception:
        pass

    try:
        app.grant(
            "com.huawei.android.launcher.permission.READ_SETTINGS",
            mode=GrantType.GRANT_ALLOW,
        )
    except Exception:
        pass

    try:
        app.grant(
            "com.huawei.android.launcher.permission.WRITE_SETTINGS",
            mode=GrantType.GRANT_ALLOW,
        )
    except Exception:
        pass

    try:
        app.grant("android.permission.READ_APP_BADGE", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant(
            "com.oppo.launcher.permission.READ_SETTINGS", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant(
            "com.oppo.launcher.permission.WRITE_SETTINGS", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass

    try:
        app.grant("android.permission.READ_SYNC_SETTINGS", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.WRITE_SYNC_SETTINGS", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant("android.permission.GET_ACCOUNTS", mode=GrantType.GRANT_ALLOW)
    except Exception:
        pass

    try:
        app.grant(
            "android.permission.AUTHENTICATE_ACCOUNTS", mode=GrantType.GRANT_ALLOW
        )
    except Exception:
        pass


def login(phone):
    app = d.application("org.thunderdog.challegram")
    d.start_activity(**{"component": "org.thunderdog.challegram/.MainActivity"})
    if d(text="Please enter your valid email address.").exists():
        app.reset_data()
        grant_app(d.application("org.thunderdog.challegram"))
        d.start_activity(**{"component": "org.thunderdog.challegram/.MainActivity"})
    if d(textContains="We've sent an SMS with an").exists():
        app.reset_data()
        grant_app(d.application("org.thunderdog.challegram"))
        d.start_activity(**{"component": "org.thunderdog.challegram/.MainActivity"})
    if d(textContains="send an SMS").exists():
        app.reset_data()
        grant_app(d.application("org.thunderdog.challegram"))
        d.start_activity(**{"component": "org.thunderdog.challegram/.MainActivity"})
    if d(textContains="We've sent the code to your email").exists():
        app.reset_data()
        grant_app(d.application("org.thunderdog.challegram"))
        d.start_activity(**{"component": "org.thunderdog.challegram/.MainActivity"})
    if d(textContains="code to the Telegram app on your other").exists():
        app.reset_data()
        grant_app(d.application("org.thunderdog.challegram"))
    if d(text="Enter your email address").exists():
        app.reset_data()
        grant_app(d.application("org.thunderdog.challegram"))
        d.start_activity(**{"component": "org.thunderdog.challegram/.MainActivity"})
    if d(textContains="oo many request").exists():
        app.reset_data()
        grant_app(d.application("org.thunderdog.challegram"))
        d.start_activity(**{"component": "org.thunderdog.challegram/.MainActivity"})
    if d(textContains="Invalid").exists():
        app.reset_data()
        grant_app(d.application("org.thunderdog.challegram"))
        d.start_activity(**{"component": "org.thunderdog.challegram/.MainActivity"})

    time.sleep(3)
    if d(text="Start Messaging"):
        d(text="Start Messaging").click()

    phone_input = d(resourceId="org.thunderdog.challegram:id/login_phone")
    time.sleep(2)
    phone_input.set_text(phone)
    ack = d(resourceId="org.thunderdog.challegram:id/btn_done")
    ack.click()
    time.sleep(6)
    code_input = d(className="android.widget.EditText")
    time.sleep(2)
    if not d(textContains="We've sent an SMS with an").exists():
        ret_text = ""
        if d(textContains="to").exists():
            ret_text = d(textContains="to").get_text()
        if d(textContains="your").exists():
            ret_text = d(textContains="your").get_text()
        if d(textContains="oo").exists():
            ret_text = d(textContains="oo many request").get_text()
        if d(textContains="Invalid").exists():
            ret_text = d(textContains="Invalid").get_text()
        app.reset_data()
        grant_app(d.application("org.thunderdog.challegram"))
        return ret_text

    print("请输入验证码:")
    code = get_varifycation_from_remote()
    code_input.set_text(code)
    time.sleep(2)
    if d(textContains="Invalid code").exists():
        # return d(textContains="Invalid code").get_text()
        return "验证码错误"
    d(text="ALLOW").click()


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
    print(res["varify"], res["web_varify"], res["raw"])
    redis_client.setex(phone, 60, value=pickle.dumps(res))
    return res


login("13349150213")
# get_last_varifycation("8613349150214",img_path=Path("varify.png"))
