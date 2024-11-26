import asyncio
import shutil
from enum import Enum
from functools import lru_cache
from pathlib import Path

import aiofiles
from fastapi import Depends, Request, UploadFile
from fastapi.responses import FileResponse
from loguru import logger
from playwright.async_api import Playwright, async_playwright

from core.config import config
from core.const import BROSWER_STARTED
from core.db.models import App


def copy_user_data(src, dst):
    if not Path.exists(dst) and Path.exists(src):
        shutil.copytree(src, dst)
    else:
        return dst


class UserData:
    b_dir = config.broswer_data_dir

    def __init__(self, phone):
        self.phone = phone
        if not Path.exists(self.link):
            Path.mkdir(self.link, parents=True, exist_ok=True)

    @property
    def link(self) -> Path:
        path = self.b_dir / self.phone
        return Path(path)

    async def save(self, file: UploadFile):
        if file is None or file.filename is None:
            return
        path = self.link / file.filename
        async with aiofiles.open(path, "wb") as f:
            blob = await file.read()
            await f.write(blob)

    def empty(self):
        return not any(self.link.iterdir())

    def read(self):
        dir_to_zip = self.link
        if dir_to_zip.exists():
            zip_path = shutil.make_archive(self.phone, "zip", dir_to_zip)
            return FileResponse(zip_path, filename=f"{self.phone}.zip")
        else:
            return {"code": 404, "msg": "No files found"}


class Command:
    def __init__(self, cmd: list[str]) -> None:
        self.cmd = cmd

    @classmethod
    def name(cls):
        return cls.__name__

    @property
    def command(self):
        return " ".join(self.cmd)

    async def execute(self, *args, **kwargs):
        proc = await asyncio.create_subprocess_shell(self.command, *args, **kwargs)  # type: ignore
        return proc


class ChromiumBrowser(Enum):
    CHROME = "google-chrome"
    CHROME_BETA = "google-chrome-beta"
    EDGE = "microsoft-edge"
    EDGE_BETA = "microsoft-edge-beta"
    BRAVE = "brave-browser"
    OPERA = "opera"


class EdgeCommand(Command):
    def __prework__(self):
        try:
            copy_user_data(config.basic_user_dir, self.cwd)
        except Exception as e:
            logger.error(f"Error copying user data: {e}")
            raise

    def __init__(
        self,
        phone: str,
        port: int,
        start_url: str,
        user_data_dir: Path = config.broswer_data_dir,
        *args: str,
        **kwargs: str,
    ) -> None:
        self.cwd = user_data_dir / phone
        self.__prework__()
        cmd = [
            ChromiumBrowser.EDGE_BETA.value,
            "--remote-allow-origins=*",
            start_url,
            f"--user-data-dir={self.cwd}",
            f"--remote-debugging-port={port}",
            # "--gpu=disabled",
        ]
        cmd.extend(args)
        for key, value in kwargs.items():
            cmd.append(f"--{key}={value}")
        super().__init__(cmd)

    def execute(self, *args, **kwargs):
        return super().execute(*args, **kwargs)


class Broswer:
    def __init__(self, phone):
        self.phone = phone
        self.user = UserData(phone)

    def name(self):
        return self.phone

    async def execute(self, cmd: Command):
        await cmd.execute()

    async def start(self):
        if self.user.empty():
            return "No files found"
        return "Files found"


async def connect_to_remote_browser(port, start_url):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f"{config.REMOTE_SERVER}:{port}")
        default_context = browser.contexts[0]
        page = default_context.pages[0]
        await page.goto(start_url)
        await asyncio.sleep(10)
        await page.screenshot(path="example.png")
        await page.pdf(path="example.pdf")


async def connect_to_remote_browser_with_new_context(port, start_url):
    async with async_playwright() as server:
        remoteBrowser = await server.chromium.connect_over_cdp(
            f"{config.REMOTE_SERVER}:{port}"
        )

        now = remoteBrowser.contexts[0]
        page = now.pages[0]
        await page.goto(start_url)


def transform_phone_to_port(phone: str):
    return int(phone) % 9999 + 10000  #


def compsite_command(apps: list[App]):
    phone = apps[0].phone
    port = transform_phone_to_port(phone)
    edge_port = port + 10000
    return (
        [
            EdgeCommand(
                phone=phone,
                port=edge_port,
                start_url=f"{app.login_url}",
            )
            for app in apps
        ],
        Command(
            [
                "socat",
                f"TCP-LISTEN:{port},reuseaddr,fork",
                f"TCP:localhost:{edge_port}",
            ]
        ),
        port,
    )


class self_boom_porcess:
    procss_hub = []

    @classmethod
    def register(cls, procss):
        cls.procss_hub.append(cls(procss))

    @classmethod
    def kill(cls):
        for procss in cls.procss_hub:
            procss.life_time()
            if procss.life == 0:
                procss.procss.kill()
                cls.procss_hub.remove(procss)

    def __init__(self, procss) -> None:
        self.procss = procss
        self.life = 150  #  150s, 0 means died , it will be killed

    def life_time(self):
        self.life -= 1


async def get_port(request: Request):
    item: dict = await request.json()
    app = App(**item)
    return transform_phone_to_port(app.phone)


async def run_browser(command: tuple[list[EdgeCommand], Command, int]):
    edge_start_pages, forward_command, port = command
    logger.info(f"Starting browser on port {port}")

    try:
        # Gather all the tasks
        tasks = [forward_command.execute()] + [
            edge_command.execute() for edge_command in edge_start_pages
        ]
        procs = await asyncio.wait_for(asyncio.gather(*tasks), timeout=10)
    except asyncio.TimeoutError:
        logger.error("Timeout while starting browser commands")
        return
    except Exception as e:
        logger.error(f"Error while starting browser commands: {e}")
        return
    logger.info(BROSWER_STARTED)
    await asyncio.sleep(config.BROWSER_ALIVE_TIME)
    try:
        for proc in procs:
            proc.kill()
        logger.info("All processes killed successfully")
    except ProcessLookupError:
        logger.error(
            "Close Process Error, Process not found, Maybe it has been killed."
        )
    except Exception as e:
        logger.error(f"Error while killing processes: {e}")


@lru_cache
async def get_browser_and_context(request: Request, port: int = Depends(run_browser)):
    try:
        playwright: Playwright = await async_playwright().start()
        endpoint_url = f"{config.REMOTE_PROXY}:{port}"
        browser = await playwright.chromium.connect_over_cdp(endpoint_url=endpoint_url)
    except Exception as e:
        raise Exception(e)
    else:
        context = browser.contexts[0]
        return browser, context
