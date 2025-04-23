from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = 'https://www.curseforge.com/minecraft/search?class=modpacks'

with sync_playwright() as p:
    # 启动浏览器（完整指纹模拟）
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport={'width': 1920, 'height': 1080},
    )
    page = context.new_page()

    try:
        page.goto(url, timeout=15000)
        print("页面标题:", page.title())
        
        # 提取内容
        soup = BeautifulSoup(page.content(), 'lxml')
        # 这里添加你的解析逻辑...

    except Exception as e:
        print("错误:", str(e))
    finally:
        browser.close()