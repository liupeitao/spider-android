'''
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-12-04 16:00:05
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-12-04 16:11:05
FilePath: /spider-android/core/androidspider.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from core.spider import Spider
from core.db.models import App, DeviceModel
from lamda.client import Device
from typing import Optional
class AndroidSpider(Spider):
    def __init__(self, app:App, device: Optional[DeviceModel] = None):
        super().__init__(app)
        self.device = device
        if device is None:
            raise Exception("device is None")
        if device.dtype != "android":
            raise Exception("device type is not android")
        if device.port is None:
            self.d = Device(device.ip)
        else:
            self.d = Device(device.ip, port=device.port)
        
    