import requests
import random
import time
from datetime import datetime, timedelta
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class KeepAliveService:
    def __init__(self):
        # 目标网站（仅保留 qklm.xyz 和 wyb.qklm.xyz）
        self.targets = [
            "https://qklm.xyz",
            "https://wyb.qklm.xyz"
        ]
        # 时间控制（确保12分钟内必爬取一次）
        self.max_interval = 12 * 60  # 最大间隔12分钟
        self.check_threshold = 9 * 60  # 提前3分钟检查（9+3=12）
        self.min_wait = 1 * 60  # 每次爬取后等待1-3分钟
        self.max_wait = 3 * 60
        # 记录最后访问时间（初始化为12分钟前，确保首次运行会爬取）
        self.last_visited = {url: datetime.now() - timedelta(seconds=self.max_interval) for url in self.targets}
        self.ua = UserAgent()

    def get_random_headers(self):
        # 随机请求头，模拟真实用户
        return {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": random.choice(["zh-CN,zh;q=0.9", "en-US,en;q=0.9"]),
            "Referer": random.choice(["https://www.google.com/", "https://www.baidu.com/"]),  # 来源随机
            "Connection": "keep-alive"
        }

    def simulate_visit(self, target_url):
        # 模拟用户访问：爬取主页+静态资源
        try:
            session = requests.Session()
            session.headers = self.get_random_headers()
            
            # 1. 访问主页
            response = session.get(target_url, timeout=10)
            if response.status_code != 200:
                return False
            
            # 2. 加载2-4个静态资源（CSS/JS/图片）
            soup = BeautifulSoup(response.text, "html.parser")
            assets = []
            for tag in soup.find_all(["link", "script", "img"]):
                url = tag.get("href") or tag.get("src")
                if url and (url.endswith((".css", ".js", ".png", ".jpg"))):
                    assets.append(urljoin(target_url, url))
            
            if assets:
                num_assets = random.randint(2, min(4, len(assets)))
                for asset in random.sample(assets, num_assets):
                    time.sleep(random.uniform(0.2, 1.2))  # 模拟加载延迟
                    session.get(asset, timeout=5)
            
            # 更新最后访问时间
            self.last_visited[target_url] = datetime.now()
            return True
        except:
            return False

    def select_target(self):
        # 优先爬取即将超时的网站（超过9分钟未爬取）
        now = datetime.now()
        for url in self.targets:
            elapsed = (now - self.last_visited[url]).total_seconds()
            if elapsed >= self.check_threshold:
                return url  # 优先爬取即将超时的
        # 否则随机选择一个
        return random.choice(self.targets)

    def run(self):
        # 持续爬取循环
        while True:
            target = self.select_target()
            self.simulate_visit(target)
            # 随机等待1-3分钟再下次爬取
            wait_time = random.randint(self.min_wait, self.max_wait)
            time.sleep(wait_time)