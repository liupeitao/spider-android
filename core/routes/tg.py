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
from requests import session
from core.spiders.tg.tg_regist import run

from const import RESPONSE_MSG
from core.db.models import App
from core.spiders.tg.tg_spider import TGSpider
from core.db.models import ReturnModel
from fastapi import Depends
from core.db.mgdb import get_mongo
from motor.motor_asyncio import AsyncIOMotorClient
from core.db.models import UserModel, ConfigModel 
router = APIRouter()

@router.post("/loginapp", summary="TG登录")
def tg_spider_all(background_tasks: BackgroundTasks, item: App):
    item.app = "Telegram"
    tg_spider = TGSpider(item)
    background_tasks.add_task(tg_spider.crawl_login)
    return PlainTextResponse(RESPONSE_MSG)

@router.post("/varification", summary="提取APP端的验证码")
def get_varification(background_tasks: BackgroundTasks, item: App = App()):
    item.app = "Telegram"
    tg_spider = TGSpider(item)
    r = tg_spider.get_develop_signup_code()
    return JSONResponse(r)



@router.post("/registerdev", summary="注册开发者帐号")
async def register_dev( background_tasks: BackgroundTasks, item: App = App(), mgdb_client:AsyncIOMotorClient=Depends(get_mongo)):
    item.app = "Telegram"
    db = mgdb_client.TG 
    coll = db.user
    user_exist = await coll.find_one({"phone":item.countrycode+item.phone})
    if user_exist is not None:
        user_exist = UserModel(**user_exist)
        if user_exist.registed:
            return ReturnModel(success=True, data=user_exist.model_dump(), msg="该手机号已经注册过了")
    
    try:
        res:ReturnModel = await run(phone=item.phone, countrycode=item.countrycode)
        if len(str(res.data['api_id'])) < 6:
            raise Exception(f"注册失败, {res}")
        meta_data = {
            "registed" :True,
            "session_ok":False,
            "password":"",
            "session_name": item.countrycode + item.phone,
        }
        meta_data.update(res.data)
        user_config = ConfigModel(**meta_data)
        user = UserModel(phone=item.countrycode+item.phone, registed=True, session_ok=False, api_hash=res.data['api_hash'], api_id=res.data['api_id'], config=user_config)
        try:
            await coll.insert_one(
                user.dict()
            )
        except Exception as e:
            return ReturnModel(success=False, data=res, msg=f"插入数据库没有成功{e}")
    except Exception as e:
        return ReturnModel(success=False, msg=str(e))
    else: 
        return res



@router.post("/loginsession", summary="登录")
async def login( background_tasks: BackgroundTasks, item: App, mgdb_client:AsyncIOMotorClient=Depends(get_mongo)):
    
    item.app = "Telegram" 
    db = mgdb_client.TG 
    coll = db.user
    user_exist = await coll.find_one({"phone":item.countrycode+item.phone})
    if user_exist is  None:
        return ReturnModel(success=False, msg="手机没有在数据库， 请先入库")
    user = UserModel(**user_exist)
    if not user.registed:
        return ReturnModel(success=False, msg="手机没有注册开发者帐号")
    tg_spider = TGSpider(item)
    print(tg_spider.phone)
    try:
        await tg_spider.login(user=user)
    except Exception as e:
        return ReturnModel(success=False, msg=str(e))
    else:
        coll.update_one({"phone":item.countrycode+item.phone}, {"$set":{"session_ok":True}}) 
        return ReturnModel(success=True, msg="登录成功", data=user.model_dump())
    