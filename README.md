
# 项目结构和`spider-web`， 请先熟悉`spider-web`的项目结构，然后再熟悉`spider-web`的项目结构。


本项目仅仅实现了`telegram`, 查看`core/spiders/tg/tg_spider.py` 用`lamda`做自动化实现， 
阅读`tg_spider.py`和`lamda`官方的文档， 即可理解此项目的实现。

> lamda：https://github.com/firerpa/lamda



## 运行
修改`settings.py` 中的`LAMDA_HOST` 为 `lamda`运行的手机ip地址
LAMDA_HOST = "192.168.9.7"

```bash
pip install -r requirements.txt
python app.py
```
