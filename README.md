
# 项目结构
和`spider-web`代码风格一致，由于`lamda`不支持异步， 因此和`spider-web`分成两个项目，  请先熟悉`spider-web`的项目结构，然后就知道了熟悉`spider-web`的项目结构。

> 1. `spider-web`  主要是`playwright`

> 2. `spider-android` 主要是`lamda` 

> 有用lamda和playwright不太兼容（一个同步一个异步， 为了实现最佳性能）， 因此分成两个项目。

> lamda官方：https://github.com/firerpa/lamda 


## 快速开始
修改`settings.py` 中的`LAMDA_HOST` 为 `lamda`运行的手机ip地址， 数据库地址， 晶格接收短信的接口， 日志接口等。。
LAMDA_HOST = "192.168.9.7" 详情见`settings.py`


```bash
pip install -r requirements.txt

`playwright install chromium`  # 需要创建开发者账号， 

python app.py

因为是tg所以要翻墙， 可能需要7890端口代理。
```

本项目仅仅实现了`telegram`, 和 `letstalk`  查看`core/spiders/tg/tg_spider.py` , `core/spiders/tg/letstalk_spider.py` , 他们都是用`lamda`做自动化实现， 
阅读`tg_spider.py`和`lamda`官方的文档， 即可理解此项目的实现。


## 关于tg
为了支持tg的一键登录，添加了大量的代码。
有以下几点需要注意的地方：
1. `lamda` 自动化控制手机，因为自动化对初始状态敏感，  每次都要重置应用，从而保证每次登录的流程一致。

2. `tg` 验证码发送的位置可能是邮箱，也可能是短信。
这给自动化带来了很大的麻烦。 两种获取验证码方式。

    1. 程序已经有某个邮箱的云取， 自己去邮箱中获取验证码（8613349150214我自己的手机号，就是当需要输入验证码时， 调用spider-web的gmail接口， 从gamil中获取的）。
    > 对于1， 我们也要推送验证码到前端上， 给用户确认。因此，调用晶哥的接口，把验证码给他， 他和前端交互。这段等待的时间，犹豫lamda是同步的， 要阻塞等待， 轮询某个接口，查看是否有验证码， 一般有一个超时时间。

    2. 用户直接输入验证码。
    > 对于2， 直接输入验证码， 省去了调用其他邮箱爬虫， 提取验证码的过程， 减少了bug。

3. 登录之后， 需要爬取用户的`tg`信息。 

    1. 创建开发者账号

    2. 创建开发者会话
    
    在`qctg`的`tg`养号平台中, 我们有一个接口，是爬取账号信息， 因此调用那个接口。又多了一个远端交互。
    > 上述远程接口，都在`settings.py`中有， 有了上面的说明， 应该对`settings.py`中的出现的许多url有了大概的了解。
    > 附上本条相关代码（跟随代码， 会发现流程很长。）
    ```python
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
    ```
