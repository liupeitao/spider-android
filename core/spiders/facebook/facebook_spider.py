"""
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-11-28 14:45:12
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-11-28 15:02:41
FilePath: /spider-android/android/facebook/facebook_spider.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

"""
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-11-28 14:45:12
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-11-28 14:45:14
FilePath: /spider-android/android/facebook/facebook_spider.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""
import time

from flask import cli
from lamda.client import Corner, Device, Keys, Point
from config.settings import config

def scroll_to_bottom(reverse=False):
    A = Point(x=300, y=200)
    B = Point(x=300, y=1000)
    if reverse:
        d.swipe(A, B)
    d.swipe(B, A)


def get_device():
    d = Device(config.LAMDA_HOST)
    return d


d = get_device()


def bounds_to_point(top, bottom, right):
    return Point(x=int(right / 2), y=int((top + bottom) / 2))


# r = d(className="android.view.ViewGroup", clickable=True, focusable=False)
# print(r)

# vs = [
#     i
#     for i in r.info_of_all_instances()
#     if i.visibleBounds.right == 720 and i.visibleBounds.left == 0
#     # and i.visibleBounds.bottom - i.visibleBounds.top > 140
# ]

import datetime


def scr_chat():
    r = d(
        className="android.view.ViewGroup",
        clickable=False,
        enabled=True,
        focusable=False,
    )
    vs = [
        i
        for i in r.info_of_all_instances()
        if i.visibleBounds.right == 720
        and i.visibleBounds.left == 0
        and i.visibleBounds.top > 20
    ]
    vs = vs[0:1]
    gge: str = datetime.datetime.now().strftime("%H:%M:%S")
    for index, v in enumerate(vs):
        d.screenshot(
            bound=v.bounds,
        ).save(f"static/{gge}_{index}.png")


for i in range(3):
    r = d(className="android.view.ViewGroup", clickable=True, focusable=False)

    vs = [
        i
        for i in r.info_of_all_instances()
        if i.visibleBounds.right == 720 and i.visibleBounds.left == 0
        # and i.visibleBounds.bottom - i.visibleBounds.top > 140
    ]

    for index, v in enumerate(vs):
        d.click(
            bounds_to_point(
                v.visibleBounds.top, v.visibleBounds.bottom, v.visibleBounds.right
            )
        )
        time.sleep(1)
        scr_chat()
        time.sleep(1)
        d.press_key(Keys.KEY_BACK)
        time.sleep(1)

    scroll_to_bottom()
    time.sleep(1)
