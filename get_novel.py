import requests
from lxml import etree
import os
import time
import django
import sys
from datetime import datetime
import random

# Django环境初始化
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()
from app01.models import Novel, Chapter

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://www.bqg128.com/",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
}
cookies = {
    "Hm_lvt_9c5f07b6ce20e3782eac91ed47d1421c": "1749555858",
    "Hm_lpvt_9c5f07b6ce20e3782eac91ed47d1421c": "1749555858",
    "HMACCOUNT": "3CB61739E4D65773"
}

base_url = "https://www.3d43.icu"
URLS = ['https://www.3d43.icu/html/21776/']
# 封面图片保存目录
img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'novel_covers')
os.makedirs(img_dir, exist_ok=True)

def download_image(img_url, novel_title):
    try:
        ext = os.path.splitext(img_url)[-1]
        filename = f"{novel_title}{ext}"
        local_path = os.path.join(img_dir, filename)
        r = requests.get(img_url, headers=headers, cookies=cookies, timeout=10)
        with open(local_path, 'wb') as f:
            f.write(r.content)
        # 返回/media/xxx.jpg
        return f"/media/{filename}"
    except Exception as e:
        print(f"图片下载失败: {e}")
        return ''

def parse_novel_main(html_text):
    html = etree.HTML(html_text)
    # 标题
    title = html.xpath('//meta[@property="og:novel:book_name"]/@content')
    if not title:
        title = html.xpath('//h1/text()')
    title = title[0] if title else "未知小说"
    # 作者
    author = html.xpath('//meta[@property="og:novel:author"]/@content')
    author = author[0] if author else "未知作者"
    # 简介
    description = html.xpath('//meta[@property="og:description"]/@content')
    if not description:
        description = html.xpath('//div[@class="intro"]/dl/dd/text()')
    description = description[0] if description else "暂无简介"
    # 封面
    cover_url = html.xpath('//meta[@property="og:image"]/@content')
    if not cover_url:
        cover_url = html.xpath('//div[@class="cover"]/img/@src')
    cover_url = cover_url[0] if cover_url else ''
    # 类别
    category = html.xpath('//meta[@property="og:novel:category"]/@content')
    category = category[0] if category else "其他"
    # 小说内容（可后续拼接所有章节内容）
    content = ""
    # 下载封面
    local_cover = download_image(cover_url, title) if cover_url else ''
    return {
        "title": title,
        "author": author,
        "description": description,
        "cover_url": local_cover,
        "category": category,
        "content": content
    }

def parse_chapter_page(html_text):
    html = etree.HTML(html_text)
    # 章节标题
    title = html.xpath('//h1[@class="wap_none"]/text()')
    if not title:
        title = html.xpath('//span[@class="title"]/text()')
    title = title[0] if title else "未知章节"
    # 章节内容
    content_list = html.xpath('//div[@id="chaptercontent"]//text()')
    content = ''.join(content_list).replace('\xa0', '').replace('\r', '').replace('\n', '').strip()
    if not content:
        content = "暂无内容"
    return {
        "chapter_title": title,
        "chapter_content": content
    }

def main():
    for novel_url in URLS:
        try:
            resp = requests.get(novel_url, headers=headers, cookies=cookies)
            novel_info = parse_novel_main(resp.text)
            # 取小说编号
            novel_id = novel_url.rstrip('/').split('/')[-1]
            # 保存小说信息到数据库（如不存在则新建）
            novel_obj, created = Novel.objects.get_or_create(
                title=novel_info['title'],
                defaults={
                    'author': novel_info['author'],
                    'description': novel_info['description'],
                    'cover_url': novel_info['cover_url'],
                    'category': novel_info['category'],
                    'content': novel_info['content'],
                    'created_at': datetime.now(),
                    'updated_at': datetime.now(),
                }
            )
            # 只爬取前30章
            for i in range(1, 31):
                chapter_url = f"{base_url}/html/{novel_id}/{i}.html"
                try:
                    resp = requests.get(chapter_url, headers=headers, cookies=cookies, timeout=15)
                    chapter_data = parse_chapter_page(resp.text)
                    Chapter.objects.create(
                        novel=novel_obj,
                        title=chapter_data['chapter_title'],
                        content=chapter_data['chapter_content'],
                        price=0.00,
                        created_at=datetime.now()
                    )
                    print(f"已保存: {novel_info['title']} - {chapter_data['chapter_title']}")
                    time.sleep(random.randint(2, 5))
                except Exception as e:
                    print(f"章节爬取失败: {chapter_url}, 错误: {e}")
        except Exception as e:
            print(f"小说主页爬取失败: {novel_url}, 错误: {e}")

if __name__ == '__main__':
    main()