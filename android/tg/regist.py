
from l.rediscli import get_redis_client
import time

redis_cli = get_redis_client()
def input_phone(page, phone):
    print("手机号")
    page.locator('#my_login_phone').fill(phone)
    
def click_fill_api_info(page):
    print("完善API信息")
    page.locator('a:has-text("API development tools")').click()

def get_verification_code(page):
    print("获取验证码")
    submit = page.locator('button:has-text("Next")')
    submit.click()

def input_verification_code(page, code):
    print("验证码提交")
    page.locator('#my_password').fill(code)
    # <a href="/apps">API development tools</a>


def sing_in(page):
    sign_in = page.locator('button:has-text("Sign In")')
    sign_in.click()
    # 18143925451
    # <a href="/apps">API development tools</a>\

# app_title
def fill_app_title(page, title):
    print(f"应用标题:{title}")
    page.locator('#app_title').fill(title)

def fill_app_short_name(page, short_name):
    print(f"应用简称:{fill_app_short_name}")
    page.locator('#app_shortname').fill(short_name)


def create_app(page):
    print("创建应用")
    try:
        page.locator('button:has-text("Create application")').click()   
        print("开发者帐号创建成功")
        return True
    except Exception as e:
        return False

  

def run(playwright, phone):
    browser = playwright.chromium.launch(headless=True)  
    context = browser.new_context()  
    page = context.new_page()  
    page.goto("https://my.telegram.org/auth")  
    page.wait_for_timeout(4000)  
    input_phone(page, phone)
    get_verification_code(page)
    page.wait_for_timeout(2000)  
    # verification_code = input("输入登录密码:")
    i = 0
    while i < 100:
        verification_code = redis_cli.get(phone)
        print(verification_code)
        if verification_code:
            redis_cli.delete(phone)
            break
        time.sleep(1)
        i+=1

    input_verification_code(page, verification_code)
    sing_in(page)
    page.wait_for_timeout(3000) 
    click_fill_api_info(page)
    page.wait_for_timeout(2000)
    fill_app_title(page, "fjlkdsfsdjfls")  
    page.wait_for_timeout(2000)
    fill_app_short_name(page, "fjlkdsfgg")
    page.wait_for_timeout(2000)
    
    if not create_app(page):
        print("创建失败")
        return "该手机号已经注册过了"
    page.wait_for_timeout(3000)
    source = page.content()
    print(source)
    
    with open(f"{phone}.html", "w") as f:
        f.write(source)

    page.screenshot(path=f"{phone}.png")

    page.wait_for_timeout(3)
    return source
    



# phone = "19194910643"
# with sync_playwright() as playwright:
#     run(playwright, phone=phone) 
