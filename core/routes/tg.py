'''
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-12-04 09:34:42
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-12-04 15:46:03
FilePath: /spider-android/routers/tg.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import PlainTextResponse, JSONResponse
from core.spiders.tg.tg_regist import run

from const import RESPONSE_MSG
from core.db.models import App
from core.spiders.tg.tg_spider import TGSpider

router = APIRouter()


@router.post("/", summary="TG登录")
def tg_spider_all(background_tasks: BackgroundTasks, item: App):
    item.app = "Telegram"
    tg_spider = TGSpider(item)
    background_tasks.add_task(tg_spider.crawl_login)
    return PlainTextResponse(RESPONSE_MSG)

@router.post("/varification", summary="提取APP端的验证码")
def get_varification(background_tasks: BackgroundTasks, item: App):
    item.app = "Telegram"
    tg_spider = TGSpider(item)
    r = tg_spider.get_develop_signup_code()
    return JSONResponse(r)


@router.post("/registerdev", summary="注册开发者帐号")
async def register_dev(background_tasks: BackgroundTasks, item: App):
    item.app = "Telegram"
    res = await run(phone=item.phone, countrycode=item.countrycode)
    return res
    