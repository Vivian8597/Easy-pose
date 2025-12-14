import requests
from bs4 import BeautifulSoup
import random

class ImageSearcher:
    def __init__(self):
        # 初始化搜索引擎URL和headers
        self.search_engines = [
            'https://www.bing.com/images/search?q={}',
            'https://duckduckgo.com/?q={}&iax=images&ia=images'
        ]
        
        # 请求头，模拟浏览器访问
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Unsplash API配置（可选，需要注册获取API密钥）
        self.unsplash_api_key = None  # 请替换为您的Unsplash API密钥
        self.unsplash_api_url = 'https://api.unsplash.com/search/photos'
    
    def search_images(self, keywords, limit=5):
        """
        根据关键词搜索图片
        :param keywords: 搜索关键词列表
        :param limit: 返回结果数量
        :return: 图片URL列表
        """
        # 将关键词列表转换为字符串
        search_query = ' '.join(keywords)
        
        # 尝试使用Unsplash API（如果有API密钥）
        if self.unsplash_api_key:
            try:
                images = self._search_unsplash(search_query, limit)
                if images:
                    return images
            except Exception as e:
                print(f"Unsplash API error: {e}")
                # 如果Unsplash API失败，回退到搜索引擎
        
        # 使用搜索引擎搜索
        return self._search_web(search_query, limit)
    
    def _search_unsplash(self, query, limit=5):
        """
        使用Unsplash API搜索图片
        :param query: 搜索查询
        :param limit: 返回结果数量
        :return: 图片URL列表
        """
        params = {
            'query': query,
            'per_page': limit,
            'orientation': 'portrait'
        }
        
        headers = {
            'Authorization': f'Client-ID {self.unsplash_api_key}',
            'Accept-Version': 'v1'
        }
        
        response = requests.get(self.unsplash_api_url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        images = []
        
        for result in data.get('results', []):
            images.append({
                'url': result['urls']['regular'],
                'thumbnail': result['urls']['small'],
                'source': 'unsplash',
                'photographer': result['user']['name']
            })
        
        return images
    
    def _search_web(self, query, limit=5):
        """
        使用网页搜索引擎搜索图片
        :param query: 搜索查询
        :param limit: 返回结果数量
        :return: 图片URL列表
        """
        # 随机选择一个搜索引擎
        search_url = random.choice(self.search_engines).format(query.replace(' ', '+'))
        
        try:
            # 发送请求
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取图片URL
            images = []
            
            # 根据不同搜索引擎的HTML结构提取图片
            if 'bing' in search_url:
                images = self._extract_bing_images(soup, limit)
            elif 'duckduckgo' in search_url:
                images = self._extract_duckduckgo_images(soup, limit)
            
            return images
            
        except Exception as e:
            print(f"Web search error: {e}")
            return []
    
    def _extract_bing_images(self, soup, limit=5):
        """
        从Bing图片搜索结果中提取图片URL
        :param soup: BeautifulSoup对象
        :param limit: 返回结果数量
        :return: 图片URL列表
        """
        images = []
        
        # Bing图片搜索结果的HTML结构
        img_elements = soup.find_all('img', class_='mimg')
        
        for img in img_elements[:limit]:
            img_url = img.get('src') or img.get('data-src')
            if img_url and img_url.startswith('http'):
                images.append({
                    'url': img_url,
                    'thumbnail': img_url,
                    'source': 'bing',
                    'photographer': 'Unknown'
                })
        
        return images
    
    def _extract_duckduckgo_images(self, soup, limit=5):
        """
        从DuckDuckGo图片搜索结果中提取图片URL
        :param soup: BeautifulSoup对象
        :param limit: 返回结果数量
        :return: 图片URL列表
        """
        images = []
        
        # DuckDuckGo图片搜索结果的HTML结构
        img_elements = soup.find_all('img', class_='tile--img__img')
        
        for img in img_elements[:limit]:
            img_url = img.get('src') or img.get('data-src')
            if img_url and img_url.startswith('http'):
                images.append({
                    'url': img_url,
                    'thumbnail': img_url,
                    'source': 'duckduckgo',
                    'photographer': 'Unknown'
                })
        
        return images
    
    def set_unsplash_api_key(self, api_key):
        """
        设置Unsplash API密钥
        :param api_key: Unsplash API密钥
        """
        self.unsplash_api_key = api_key
