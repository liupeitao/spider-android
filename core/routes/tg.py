'''
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-12-04 09:34:42
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-12-04 15:46:03
FilePath: /spider-android/routers/tg.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import asyncio
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import PlainTextResponse, JSONResponse
import requests
from core.spiders.tg.tg_regist import run

from const import RESPONSE_MSG
from core.db.models import App
from core.spiders.tg.tg_spider import TGSpider
from core.db.models import ReturnModel
from fastapi import Depends
from core.db.mgdb import get_mongo
from motor.motor_asyncio import AsyncIOMotorClient
from core.db.models import UserModel, ConfigModel 
from config.settings import config
router = APIRouter()

@router.post("/loginapp", summary="TG登录")
async def login_tg(item: App):
    item.app = "Telegram"
    tg_spider =  TGSpider(item)
    await asyncio.to_thread(tg_spider.crawl_login)
    return PlainTextResponse(RESPONSE_MSG)

@router.post("/varification", summary="提取APP端的验证码")
def get_varification(background_tasks: BackgroundTasks, item: App = App()):
    item.app = "Telegram"
    tg_spider = TGSpider(item)
    r = tg_spider.get_develop_signup_code()
    return JSONResponse(r)

@router.post("/registerdev", summary="注册开发者帐号")
async def register_dev( item: App = App(), mgdb_client:AsyncIOMotorClient=Depends(get_mongo)):
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
            "session_name": item.countrycode + item.phone,
        }
        meta_data.update(res.data)
        user_config = ConfigModel(**meta_data)
        user = UserModel(phone=item.countrycode+item.phone, category="sync",  registed=True, session_ok=False, api_hash=res.data['api_hash'], api_id=res.data['api_id'], config=user_config)
        try:
            await coll.insert_one(
                user.dict()
            )
        except Exception as e:
            g = await coll.find_one({"phone":item.countrycode+item.phone})
            if g is not None:
                raise Exception(f"插入数据库没有成功{e}")
            else:
                pass
    except Exception as e:
        raise Exception(f"注册失败, {e}")
    else: 
        return res

@router.post("/loginsession", summary="登录")
async def login_session(  item: App, mgdb_client:AsyncIOMotorClient=Depends(get_mongo)):
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

async def mock_register_dev(item:App, mdgb_client:AsyncIOMotorClient):
    item.app = "Telegram"
    db = mdgb_client.TG 
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
            "session_name": item.countrycode + item.phone,
        }
        meta_data.update(res.data)
        user_config = ConfigModel(**meta_data)
        user = UserModel(phone=item.countrycode+item.phone, category="sync", registed=True, session_ok=False, api_hash=res.data['api_hash'], api_id=res.data['api_id'], config=user_config)
        try:
            await coll.insert_one(
                user.dict()
            )
        except Exception as e:
            g = await coll.find_one({"phone":item.countrycode+item.phone})
            if g is not None:
                raise Exception(f"插入数据库没有成功{e}")
            else:
                pass
    except Exception as e:
        raise Exception(f"注册失败, {e}")
    else: 
        return res

async def mock_login_ssession(item:App, mgdb_client:AsyncIOMotorClient):
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
    
@router.post("/tg", summary="获取session")
async def gather(item: App, mgdb_client:AsyncIOMotorClient=Depends(get_mongo)):
    try:
        # 第二步：注册开发者账号
        dev_response = await  mock_register_dev(item, mgdb_client)
        if not dev_response.success:
            return dev_response
        # 第三步：登录session,已经成功了， 调用qctg即可
        session_response = await mock_login_ssession(item, mgdb_client)
        if not session_response.success:
            return session_response
        # 第四步：开始下载
        print(f"开始下载,路由到{config.RUN_TG_URL}")
        requests.post(config.RUN_TG_URL,   json={"phone": item.phone, "run_types": ["dialogs", "chats", "members"]})
    except Exception as e:
        return ReturnModel(success=False, msg=f"获取session失败: {str(e)}")