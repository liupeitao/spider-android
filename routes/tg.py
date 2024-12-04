'''
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-12-04 09:34:42
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-12-04 10:04:26
FilePath: /spider-android/routers/tg.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import PlainTextResponse

from const import RESPONSE_MSG
from db.models import App
from android.tg.tg_spider import TGSpider

router = APIRouter()


@router.post("/", summary="TG登录")
def taobao_spider_all(background_tasks: BackgroundTasks, item: App):
    item.app = "Telegram"
    tg_spider = TGSpider(item)
    background_tasks.add_task(tg_spider.crawl_login)
    return PlainTextResponse(RESPONSE_MSG)
