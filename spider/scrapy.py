import cloudscraper
import time
from bs4 import BeautifulSoup

# 目标 URL
url = 'https://www.curseforge.com/minecraft/search?class=modpacks'

# 配置完整的浏览器级请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.curseforge.com/',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
}

# 初始化 Cloudscraper（启用自动解析浏览器指纹）
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False,
        'desktop': True,
    }
)

try:
    # 添加随机延迟（模拟人类操作）
    time.sleep(2)

    # 发送请求（携带完整请求头）
    response = scraper.get(url, headers=headers)

    # 输出状态码和标题
    print("状态码:", response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        title_tag = soup.find('title')
        print("页面标题:", title_tag.get_text() if title_tag else "无标题")
    else:
        print("响应内容片段:", response.text[:200])  # 查看是否被重定向到验证页面

except Exception as e:
    print("请求异常:", str(e))