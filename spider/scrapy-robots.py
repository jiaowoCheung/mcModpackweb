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
        
    def check_robots_txt(self):
        """检查robots.txt权限"""
        self.rp.set_url(f"{self.base_url}/robots.txt")
        try:
            self.rp.read()
            return self.rp.can_fetch("*", self.base_url + self.target_path)
        except Exception as e:
            print(f"检查robots.txt失败: {e}")
            return True  # 如果无法读取则默认允许

    def crawl(self):
        if not self.check_robots_txt():
            print("当前页面不允许爬取，请检查robots.txt限制")
            return []
            
        results = []
        page = 1
        max_retry = 3
        
        while True:
            url = f"{self.base_url}{self.target_path}?&page={page}" if page > 1 else f"{self.base_url}{self.target_path}"
            
            for attempt in range(max_retry):
                try:
                    print(f"正在爬取第 {page} 页 ({attempt+1}/{max_retry})")
                    soup = self.fetch_page(url)
                    if not soup:
                        continue
                        
                    data = self.extract_data(soup)
                    if not data:
                        return results  # 没有数据表示到达末页
                        
                    results.extend(data)
                    time.sleep(random.uniform(1.5, 3.5))  # 更随机的延迟
                    break
                except Exception as e:
                    print(f"第 {page} 页尝试 {attempt+1} 失败: {str(e)}")
                    if attempt == max_retry - 1:
                        return results
                    time.sleep(5 * (attempt + 1))
            
            page += 1

    def fetch_page(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            # 检查是否被重定向到禁止页面
            if response.url != url and "disallowed" in response.url.lower():
                print(f"被重定向到禁止页面: {response.url}")
                return None
                
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {str(e)}")
            return None

    def extract_data(self, soup):
        data = []
        items = soup.select('.modlist-block .title p.name a')
        for item in items:
            text = item.get_text(strip=True)
            if text:
                data.append(text)
        return data

if __name__ == "__main__":
    start = time.time()
    crawler = MCMODCrawler()
    results = crawler.crawl()
    
    print(f"\n爬取完成，共获取 {len(results)} 条数据，耗时 {time.time()-start:.1f}秒")
    print("前10条结果示例:")
    for i, item in enumerate(results[:10], 1):
        print(f"{i}. {item}")
    
    # 保存结果到文件
    with open("mcmod_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    print("结果已保存到 mcmod_results.txt")