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
from core.db.models import ReturnModel
from fastapi import Depends
from core.db.mgdb import get_mongo
from motor.motor_asyncio import AsyncIOMotorClient
router = APIRouter()


@router.post("/loginapp", summary="TG登录")
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
async def register_dev( background_tasks: BackgroundTasks, item: App, mgdb_client:AsyncIOMotorClient=Depends(get_mongo)):
    item.app = "Telegram"
    try:
        res = await run(phone=item.phone, countrycode=item.countrycode)
        db = mgdb_client.TG 
        coll = db.user
        meta_data = {
            "registed" :True,
            "session_ok":False,
            "password":""
        }
        meta_data.update(res.data)
        try:
            coll.insert_one({
                meta_data
            })
        except Exception:
            return res
    except Exception as e:
        return ReturnModel(success=False, msg=str(e))
    else: 
        return res


@router.post("/loginsession", summary="登录")
async def login( background_tasks: BackgroundTasks, item: App, mgdb_client:AsyncIOMotorClient=Depends(get_mongo)):
    item.app = "Telegram" 
    tg_spider = TGSpider(item)
    print(tg_spider.phone)
    try:
        await tg_spider.login()
    except Exception as e:
        return ReturnModel(success=False, msg=str(e))
    else:
        return ReturnModel(success=True, msg="登录成功")
    