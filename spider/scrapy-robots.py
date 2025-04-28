import json  
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.robotparser import RobotFileParser

class MCMODCrawler:
    def __init__(self):
        self.base_url = "https://www.mcmod.cn"
        self.target_path = "/modpack.html"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': self.base_url
        }
        self.rp = RobotFileParser()
        self.max_pages = 20
        self.max_items = 200
        
    def check_robots_txt(self):
        self.rp.set_url(f"{self.base_url}/robots.txt")
        try:
            self.rp.read()
            return self.rp.can_fetch("*", self.base_url + self.target_path)
        except Exception as e:
            print(f"检查robots.txt失败: {e}")
            return True

    def crawl(self):
        if not self.check_robots_txt():
            print("当前页面不允许爬取，请检查robots.txt限制")
            return []
            
        results = []
        page = 1
        max_retry = 3
        
        while page <= self.max_pages and len(results) < self.max_items:
            url = f"{self.base_url}{self.target_path}?page={page}" if page > 1 else f"{self.base_url}{self.target_path}"
            
            page_success = False  # 标记当前页是否成功爬取
            for attempt in range(max_retry):
                try:
                    print(f"正在爬取第 {page} 页 ({attempt+1}/{max_retry})")
                    soup = self.fetch_page(url)
                    if not soup:
                        continue
                        
                    page_data = self.extract_data(soup)
                    if not page_data:
                        print(f"第 {page} 页无数据，停止爬取")
                        return results  # 返回已爬取的数据
                        
                    results.extend(page_data)
                    time.sleep(random.uniform(1.5, 3.5))
                    page_success = True
                    break  # 爬取成功，跳出重试循环
                except Exception as e:
                    print(f"第 {page} 页尝试 {attempt+1} 失败: {str(e)}")
                    if attempt == max_retry - 1:
                        print(f"第 {page} 页重试次数用尽，跳过此页")
                    time.sleep(5 * (attempt + 1))
            
            if not page_success:
                print(f"第 {page} 页爬取失败，终止爬虫")
                return results  # 直接返回已爬取的数据
            
            page += 1
        
        return results  # 正常循环结束返回数据

    def fetch_page(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            if response.url != url and "disallowed" in response.url.lower():
                print(f"被重定向到禁止页面: {response.url}")
                return None
                
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {str(e)}")
            return None

    def extract_data(self, soup):
        items = []
        blocks = soup.select('.modlist-block')
        
        for block in blocks:
            title_elem = block.select_one('.title p.name a')
            link_elem = block.select_one('.cover a[href]')
            picture=block.select_one('.cover a img[src]')
            
            if not title_elem or not link_elem:
                continue
                
            raw_link = link_elem.get('href')
            full_link = f"{self.base_url}{raw_link}" if raw_link.startswith('/') else raw_link
            
            items.append({
                "text": title_elem.get_text(strip=True),
                "link": full_link,
                'img':picture.get('src') if picture else None
            })
        
        return items

if __name__ == "__main__":
    start = time.time()
    crawler = MCMODCrawler()
    results = crawler.crawl()
    
    # 确保结果始终为列表
    if not isinstance(results, list):
        results = []
    
    print(f"\n爬取完成，共获取 {len(results)} 条数据，耗时 {time.time()-start:.1f}秒")
    print("前5条结果示例:")
    for i, item in enumerate(results[:5], 1):
        print(f"{i}. 文本: {item['text']}")
        print(f"   链接: {item['link']}\n")
    
    with open("mcmod_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("结果已保存到 mcmod_data.json")