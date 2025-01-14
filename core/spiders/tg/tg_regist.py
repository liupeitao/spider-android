import asyncio
import requests

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from config.settings import config
from core.db.models import ReturnModel

def parse_api_info(source):
    res = {}
    soup = BeautifulSoup(source, "html.parser")
    try:
        for index, i in enumerate(soup.find_all("div", class_="form-group")[0:2]):
            r = i.get_text().replace("App", "").replace("\n", "")
            if index == 0:
                try:
                    res["api_id"] = int(r.split(":")[1].strip())
                except Exception:
                    res["api_id"] = 0
            else:
                res["api_hash"] = r.split(":")[1].strip()
        return res["api_id"], res["api_hash"]
    except IndexError:
        raise Exception("解析失败")


async def input_phone(page, phone):
    print("手机号")
    await page.locator("#my_login_phone").fill(phone)


async def click_fill_api_info(page):
    print("完善API信息")
    await page.locator('a:has-text("API development tools")').click()


async def get_verification_code(page):
    print("获取验证码")
    submit = page.locator('button:has-text("Next")')
    await submit.click()
    await page.wait_for_timeout(2000)
    content = await page.content()
    if "tries" in content:
        raise Exception("请求过于频繁. 请稍后再试")


async def input_verification_code(page, code):
    print("验证码提交")
    await page.locator("#my_password").fill(code)
    await asyncio.sleep(1)
    # <a href="/apps">API development tools</a>


async def sing_in(page):
    sign_in = page.locator('button:has-text("Sign In")')
    await sign_in.click()
    await asyncio.sleep(2)
    content = await page.content()
    if "Invalid" in content:
        raise Exception("验证码错误")

    # 18143925451
    # <a href="/apps">API development tools</a>\


# app_title
async def fill_app_title(page, title):
    print(f"应用标题:{title}")
    await page.locator("#app_title").fill(title)


async def check_registed(page):
    api_id, api_hash = parse_api_info(await page.content())
    if api_id and int(api_id) and len(api_hash) > 20 and "alphanumeric" not in api_hash:
        return True
    return False


async def fill_app_short_name(page, short_name):
    print(f"应用简称:{short_name}")
    await page.locator("#app_shortname").fill(short_name)


async def create_app(page):
    print("创建应用")
    try:
        await page.locator('button:has-text("Create application")').click()
        print("开发者帐号创建成功")
        return True
    except Exception:
        return False




def requests_varify_code(phone, countrycode):
    #TODO 验证码
    resp = requests.post(
        config.TG_VERIFICATION_CODE_URL,
        json={
            "app": "Amap",
            "countrycode": countrycode,
            "phone": phone,
            "task_uid": "2517d19b-5fea-4aaa-8b2a-d3964e61a1a3",
        },
    )
    print(resp.json()['web_varify']['code'])
    return resp.json()['web_varify']['code']



async def _run(playwright, phone, countrycode):
    print("开始注册")
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://my.telegram.org/auth")
    await page.wait_for_timeout(4000)
    await input_phone(page, countrycode+phone)
    await get_verification_code(page)
    await page.wait_for_timeout(2000)
    print("输入验证码")
    await asyncio.sleep(7) # 等待7s是为了过提醒
    verification_code = requests_varify_code(phone=phone, countrycode=countrycode)
    print(f"提取的验证码是:{verification_code}")
    await input_verification_code(page, verification_code)
    await sing_in(page)
    await page.wait_for_timeout(3000)
    await click_fill_api_info(
        page,
    )
    await page.wait_for_timeout(2000)
    print("检查是否注册过")
    try:
        registed = await check_registed(page)
    except Exception:
        pass
    else:
        if registed:
            api_id, api_hash = parse_api_info(await page.content())
            print("该手机号已经注册过了")
            print({"phone": countrycode+phone, "api_id": api_id, "api_hash": api_hash})
            r_json = {"phone": countrycode+phone, "api_id": api_id, "api_hash": api_hash}
            return ReturnModel(data=r_json, success=True)
    await fill_app_title(page, "fjlkdsfsdjfls")
    await page.wait_for_timeout(2000)
    await fill_app_short_name(page, "fjlkdsfgg")
    await page.wait_for_timeout(2000)

    if not await create_app(page):
        raise Exception("创建失败")
    await page.wait_for_timeout(3000)
    source = await page.content()
    api_id, api_hash = parse_api_info(source)
    print({"phone": countrycode+phone, "api_id": api_id, "api_hash": api_hash})
    if api_id == 0:
        raise Exception("注册失败")
    r_json = {"phone": countrycode+phone, "api_id": api_id, "api_hash": api_hash}
    return ReturnModel(data=r_json, success=True)

async def run(phone, countrycode)-> ReturnModel:
    try:
        async with async_playwright() as playwright:
            res = await _run(playwright, phone=phone, countrycode=countrycode)
            return res
    except Exception as e:
        raise Exception(f"注册失败{e}")
