'''
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-11-26 17:43:56
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-12-04 09:43:33
FilePath: /spider-android/const.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
BROSWER_STARTED = "Browser in the server side started successfully"
CLEAN_PROCESS = "All processes killed successfully"  # 当浏览器超时， 或者其他原因导致退出时， 会打印这个信息。
NONECONTENT = "没有内容"  # crawl_xxx方法结果为空时，会抛出这个异常
TASKTIMEOUT = "任务处理超时"  #  crawl_xxx任务处理超时时，会抛出这个异常
NONEBROWSER = "Browser is None"  # 没有浏览器， 原因 1. 启动失败， 2 已经关闭
NONERESPONSE = "Response is None"  # 没有响应， 原因 1. 页面加载失败， 2. 页面加载超时


RESPONSE_MSG = "后台运行中"  # 返回给前端的默认值


#### URLS
CRAWLER_DEFINE = {
    "MeiTuan": "美团",
    "LaGou": "拉勾网",
    "Ems": "邮政EMS",
    "Yto": "圆通速递",
    "YunDaSy": "韵达速递",
    "Zto": "中通速递",
    "Train12306": "12306",
    "CowTransfer": "奶牛快传",
    "Qunar": "去哪儿网",
    "Baidu": "百度",
    "SF_Express": "顺丰速运",
    "office365": "office365",
    "MailYeah": "yeah邮箱",
    "Mail126": "126邮箱",
    "Ele": "饿了么",
    "Gmail": "Gmail",
    "Hotmail": "hotmail邮箱",
    "MailQQ": "QQ邮箱",
    "Mail163": "163邮箱",
    "Mail139": "139邮箱",
    "YangKeDuo": "拼多多",
    "Aliyunpan": "阿里云盘",
    "DingDing": "钉钉",
    "huaweiyun": "华为云空间",
    "BaiDuditu": "百度地图",
    "Instagram": "Instagram",
    "CaiNiaoguoguo": "菜鸟裹裹",
    "AliPay": "支付宝",
    "HaiKanghuiyan": "海康慧眼",
    "Linkedin": "Linkedin",
    "kuaishou": "快手",
    "HuaZhu": "华住",
    "Amap": "高德地图",
    "MiJia": "米家",
    "JD": "京东",
    "TaoBao": "淘宝",
    "Ctrip": "携程",
    "Ly": "同程旅行",
    "DiDiTaxi": "滴滴出行",
    "Skype": "Skype",
    "CamScanner": "扫描全能王",
    "OneDrive": "OneDrive",
    "Twitter": "Twitter",
    "SinaEmail": "新浪邮箱",
    "Mail189": "189邮箱",
    "ZohoMail": "ZohoMail",
    "YaHoo": "雅虎",
    "oppoyun": "oppo云服务",
    "DouYin": "抖音",
    "vivoyun": " vivo云服务",
    "WB": "新浪微博",
    "Telegram":"Telegram"
}