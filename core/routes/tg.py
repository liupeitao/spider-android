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
from fastapi.responses import  JSONResponse
import requests
from core.spiders.tg.tg_regist import run

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
async def login_tg(item: App, background_tasks: BackgroundTasks):
    item.app = "Telegram"
    tg_spider =  TGSpider(item)
    # await asyncio.to_thread(tg_spider.crawl_login)
    background_tasks.add_task(tg_spider.crawl_login)
    return ReturnModel(success=True, msg="后台处理中，请稍后查看结果")

@router.post("/varification", summary="提取APP端的验证码")
def get_varification(background_tasks: BackgroundTasks, item: App = App()):
    item.app = "Telegram"
    tg_spider = TGSpider(item)
    r = tg_spider.crawl_verify()
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
        await tg_spider.crawl_session(user=user)
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
        res = await run(phone=item.phone, countrycode=item.countrycode)
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
    if user.session_ok:
        return ReturnModel(success=True, msg="已经登录过了, 无需再次登录")
    tg_spider = TGSpider(item)
    print(tg_spider.phone)
    try:
        await tg_spider.crawl_session(user=user)
    except Exception as e:
        return ReturnModel(success=False, msg=str(e))
    else:
        coll.update_one({"phone":item.countrycode+item.phone}, {"$set":{"session_ok":True}}) 
        return ReturnModel(success=True, msg="登录成功", data=user.model_dump())
    
async def procedure(item: App, mgdb_client:AsyncIOMotorClient):
    try:
        # 第1步：注册开发者账号
        dev_response = await  mock_register_dev(item, mgdb_client)
        if not dev_response.success:
            raise Exception(dev_response.msg)
        # 第2步：创建tg session
        session_response = await mock_login_ssession(item, mgdb_client)
        if not session_response.success:
            raise Exception(session_response.msg)
        # TODO: 第3步， 调用qctg接口， 它会 利用session获取数据
        # 第3步， 调用qctg接口， 它会 利用session获取数据
        print(f"给后台发送爬取请求{config.RUN_TG_URL}")
        response = requests.post(
                f"{config.RUN_TG_URL}",
                json={"phone": item.countrycode+item.phone, "run_types": ["dialogs", "chats", "members"]},
                timeout=300
        )
        print("后台爬取中")
    except Exception as e:
        return ReturnModel(success=False, msg=f"获取session失败: {str(e)}")
    else:
        return ReturnModel(success=True, msg="获取session成功", data=session_response.data)

@router.post("/getdata", summary="获取session")
async def gather(item: App, mgdb_client:AsyncIOMotorClient=Depends(get_mongo), background_tasks: BackgroundTasks = None):
    background_tasks.add_task(procedure, item, mgdb_client)
    return ReturnModel(success=True, msg="后台处理中，请稍后查看结果")
    