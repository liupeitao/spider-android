'''
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-11-26 17:43:56
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-12-04 10:10:51
FilePath: /spider-android/tools/logger.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   log_config.py
@Time    :   2024/06/18 16:32:36
@Author  :   Jingjing-Zhu
@Email   :   1079677051@qq.com
"""

import os
from pathlib import Path
from sys import stdout

from loguru import logger


def creat_customize_log_loguru(pro_path=None):
    """
    :param pro_path:  当前需要生产的日志文件的存在路径
    :return:
    """
    logger.info("开始构建日志")
    if not pro_path:
        LOG_PATH = Path("/var/log/qc/spider")
        # 定义info_log文件名称
        log_file_path = LOG_PATH / "log/info/{time:YYYYMM}/info_{time:YYYYMMDD}.log"
        # 定义err_log文件名称
        err_log_file_path = (
            LOG_PATH / "log/error/{time:YYYYMM}/error_{time:YYYYMMDD}.log"
        )
    else:
        # 定义info_log文件名称
        log_file_path = os.path.join(pro_path, "log/info_{time:YYYYMMDD}.log")
        # 定义err_log文件名称
        err_log_file_path = os.path.join(pro_path, "log/error_{time:YYYYMMDD}.log")

    LOGURU_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>|<level>{level: <6}</level>|{name}:{line}|<bold>{message}</bold>"
    # 这句话很关键避免多次的写入我们的日志
    logger.configure(handlers=[{"sink": stdout, "format": LOGURU_FORMAT}])
    # 对应不同的格式
    info_format = "<green>{time:YYYY-MM-DD HH:mm:ss:SSS}</green>|{name}:{line}|process_id:{process.id} process_name:{process.name} | thread_id:{thread.id} thread_name:{thread.name} | {level} | {message}"
    logger.add(
        log_file_path,
        format=info_format,
        rotation="00:00",
        compression="zip",
        encoding="utf-8",
        level="INFO",
        enqueue=True,
    )
    # 错误日志不需要压缩
    error_format = "<green>{time:YYYY-MM-DD HH:mm:ss:SSS}</green>|{name}:{line}|process_id:{process.id} process_name:{process.name} | thread_id:{thread.id} thread_name:{thread.name} | {level} |\n {message}"
    logger.add(
        err_log_file_path,
        format=error_format,
        rotation="00:00",
        encoding="utf-8",
        level="ERROR",
        enqueue=True,
    )
