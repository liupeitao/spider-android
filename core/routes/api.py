'''
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-11-26 17:43:56
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-12-04 10:02:57
FilePath: /spider-android/routes/api.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import APIRouter


from core.routes import (
    letstalk,
    tg
)

router = APIRouter()
router.include_router(letstalk.router, tags=["LetsTalk"], prefix="/LetsTalk")
router.include_router(tg.router, tags=["Telegram"], prefix="/Telegram")
