import requests
from bs4 import BeautifulSoup
import time
import random

def crawl_target_text():
    base_url = "https://www.mcmod.cn/modpack.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': base_url
    }
    
    results = []
    page = 1
    has_next_page = True
    
    while has_next_page:
        # 构造带分页参数的URL
        if page == 1:
            current_url = base_url  # 第一页不需要参数
        else:
            current_url = f"{base_url}?&page={page}"
        
        print(f"正在爬取第 {page} 页: {current_url}")  # 调试信息
        
        # 随机延迟防封禁
        time.sleep(random.uniform(1, 3))
        
        page_content = fetch_page(current_url, headers)
        if not page_content:
            break
            
        # 提取数据
        current_data = extract_data(page_content)
        if not current_data:
            has_next_page = False
        else:
            results += current_data
            page += 1
    
    return results

def fetch_page(url, headers):
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15,
            allow_redirects=False
        )
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"请求失败: {str(e)} | URL: {url}")
        return None

def extract_data(soup):
    data = []
    items = soup.select('.modlist-block .title p.name a')
    for item in items:
        text = item.get_text(strip=True)
        if text:
            data.append(text)
    return data

# 使用示例
if __name__ == "__main__":
    start = time.time()
    results = crawl_target_text()
    print(f"爬取完成，共找到 {len(results)} 条数据，耗时 {time.time()-start:.1f}秒")
    for i, text in enumerate(results[:5], 1):  # 只打印前5条示例
        print(f"{i}. {text}")