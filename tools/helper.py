import os

from loguru import logger


def banner(msg: str):
    try:
        # raise Exception("Not implemented")
        if len(msg) < 12:
            cmd = f"figlet -f slant '{msg}' | ponysay "
        else:
            cmd = f"figlet -f slant '{msg}' | lolcat"
        os.system(cmd)
    except Exception:
        logger.info(msg)
