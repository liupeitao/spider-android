from fastapi import APIRouter


from routes import (
    letstalk,
)

router = APIRouter()
router.include_router(letstalk.router, tags=["LetsTalk"], prefix="/LetsTalk")
