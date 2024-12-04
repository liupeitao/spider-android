from fastapi import APIRouter, BackgroundTasks

from core.db.models import App
from core.spiders.letstalk.letstalk_spider import LetTalk_Spider
router = APIRouter()


@router.post("/chat_history", summary="聊天记录")
async def amap_spider(item: App, background_tasks: BackgroundTasks):
    spider = LetTalk_Spider(item)
    r = spider.crawl_all_chat()
    return  r
