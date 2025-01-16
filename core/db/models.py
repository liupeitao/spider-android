import datetime
from enum import Enum
from typing import Any, Callable, Optional
from uuid import UUID
from typing import Literal

from pydantic import BaseModel, Field
from config.settings import config

class Channel(BaseModel):
    name: str

class ConfigModel(BaseModel):
    session_name: str = ""
    chats_dir: str = "chats"
    memeber_dir: str = "members"
    media_dir: str = "media"
    proxy_host: str = config.DEFAULT_PROXY_HOST
    proxy_port: int = config.DEFAULT_PROXY_PORT
    limit: int = 1000
    dialog_path: str = "dialogs"
    max_size: str = "1M"


class UserModel(BaseModel):
    phone: str = ""
    api_id: int
    api_hash: str = ""
    password: str = ""
    session_ok: bool = False  # 是否有了会话
    registed: bool = False  #  是否注册开发者。
    category: Literal['sync', 'yanghao'] = "sync"  #
    config: ConfigModel

class AppStartUrl(Enum):
    JD = "https://www.jd.com"
    JD_Order = "https://order.jd.com/center/list.action"
    JD_Cart = "https://cart.jd.com/cart_index"

    Amap = "https://www.amap.com"
    Amap_Login = "https://www.amap.com"
    Amap_History_Search = "https://www.amap.com/search/history"
    Amap_History_Buxing = "https://www.amap.com/footprint/history"
    Amap_History_Jiaotong = "https://www.amap.com/traffic/history"
    Amap_History_Dache = "https://www.amap.com/car/history"

    Qunaer = "https://www.qunar.com"
    Qunaer_Order = "https://flight.qunar.com/"

    TaoBao = "https://www.taobao.com"
    TaoBao_Order = "https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?spm=a1z0d.6639537/202406.1997525045.2.11f57484I1EwO"
    TaoBao_Cart = "https://cart.taobao.com/cart.htm?spm=a21bo.jianhua/a.1997525049.1.5af92a89X5NzNU&from=mini&ad_id=&am_id=&cm_id=&pm_id=1501036000a02c5c373"


class App(BaseModel):
    app: str = "appname"
    phone: str = "13349150214"
    task_uid: UUID = UUID("2517d19b-5fea-4aaa-8b2a-d3964e61a1a3")
    countrycode: str = "86"
    login_url: str = Field(
        default="https://www.amap.com",
    )
    port: Optional[int] = 15262
    targets: Optional[list[str]] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "app": "Amap",
                    "phone": "13349150214",
                    "task_uid": "2517d19b-5fea-4aaa-8b2a-d3964e61a1a3",
                    # "login_url": "https://www.amap.com",
                    "countrycode": "86",
                }
            ]
        }
    }


class ScrollModel(BaseModel):
    crawler: str = Field()  # which crawler to scroll
    times: int = Field(default=0, gt=0, description="How many times to scroll")
    interval: float = Field(
        default=1.0, gt=0, description="Interval between each scroll"
    )


class PageBtnModel(BaseModel):
    url: Optional[str] = None
    xpath: Optional[str] = None
    text: Optional[str] = None


class PageTurnModel(BaseModel):
    page_btn: Optional[PageBtnModel] = None
    scroll: Optional[ScrollModel] = None


class SwitchPageOpModel(BaseModel):
    page_op: Any
    crawler: str = ""
    index: int = 0


class BaseInfoModel(BaseModel):
    timestamp: str
    source: str  # app名称
    sid: str  # 机器名称
    user_phone_number: str  # 主采手机号
    phone_number: str


class CrawlerInfoModel(BaseModel):
    crawlerinfo: BaseInfoModel


class StateEnum(Enum):
    PENDING = "等待中"
    STARTING = "执行中"
    RUNNING = "运行中"
    LAUNCH_BROWSER = "打开浏览器"
    CLOSING_BROWSER = "关闭浏览器"
    OPEN_PAGE = "打开页面"
    ITERCEPT_URL = "访问接口"
    CLOSING_PAGE = "关闭页面"
    SCROLLING = "滚动页面"
    SWITCH_PAGE = "切换页面"
    SAVING = "保存结果中"
    FINISHED = "完成"
    CLEAN = "清理资源中"
    ERROR = "错误"


class ScreenShotModel(BaseModel):
    app: App
    url: str
    state: StateEnum
    base64: str


class SpiderModel(App):
    pid: int

FUNCTION_REPRESENT = {
    "chats": "聊天",
    "dialogs": "会话",
    "cart": "购物车",
    "order": "订单",
    "self": "个人信息",
    "friends": "好友",
    "follow": "关注",
    "fans": "粉丝",
    "intercept_urls": "请求接口",
    "intercept_urls_page": "请求许多接口",
    "history_dache": "打车历史记录",
    "history_jiaotong": "交通历史记录",
    "history_buxing": "步行历史记录",
    "history_search": "搜索历史记录",
    "finish": "任务执行完成",
    "start": "任务开始执行",
    "error": "执行错误",
    "dev": "注册开发者",
    "login": "登录",
    "session": "获取会话",
    "verify": "登录验证码",
}
class LogModel(BaseModel, arbitrary_types_allowed=True):
    app: App
    func: Callable
    state: StateEnum
    msg: Optional[str] = None
    create_time: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    spider: Any = None
    other: Optional[Any] = None
    exception: Optional[Exception] = None


class Verify(BaseModel):
    app: str
    countrycode: str
    phone: str
    varify: str

    

DeviceType = Literal['android', 'ios', 'web']
class DeviceModel(BaseModel):
    dtype: DeviceType
    ip: str
    port: Optional[int] = None

class ReturnModel(BaseModel):
    success: bool
    msg: str = ""
    data: Any = {}
    code: int = 200
