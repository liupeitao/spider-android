BROSWER_STARTED = "Browser in the server side started successfully"
CLEAN_PROCESS = "All processes killed successfully"  # 当浏览器超时， 或者其他原因导致退出时， 会打印这个信息。
NONECONTENT = "没有内容"  # crawl_xxx方法结果为空时，会抛出这个异常
TASKTIMEOUT = "任务处理超时"  #  crawl_xxx任务处理超时时，会抛出这个异常
NONEBROWSER = "Browser is None"  # 没有浏览器， 原因 1. 启动失败， 2 已经关闭
NONERESPONSE = "Response is None"  # 没有响应， 原因 1. 页面加载失败， 2. 页面加载超时


RESPONSE_MSG = "后台运行中"  # 返回给前端的默认值


#### URLS
