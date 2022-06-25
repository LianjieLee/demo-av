#!/usr/bin/python3
import re
import time

import requests
from bs4 import BeautifulSoup
from faker import Faker


class sehuatang:
    def __init__(self):
        self.url = 'https://www.sehuatang.net/'
        self.header = {'User-Agent': Faker().user_agent()}
        with open('old_posts.json', 'r') as f:
            self.old_posts = eval(f.read())

    # 获取一个新帖子
    def getNewPost(self):
        hd = {'Referer': 'https://www.sehuatang.net/index.php'}
        self.header.update(hd)
        r = requests.get(self.url + 'forum-103-1.html', headers=self.header)
        soup = BeautifulSoup(r.text, 'html.parser')
        thread_list = soup.find('div', {'id': 'threadlist'})
        post_list = thread_list.find_all('tbody', {'id': re.compile(r'normalthread_\d*?')})
        print(self.time(), f'抓取帖子{len(post_list)}个', flush=True)
        for i in post_list:
            thread = i.tr.td.a['href']
            if '天' not in i.tr.find('td', {'class': 'by'}).em.a.text:
                continue
            if thread not in self.old_posts:
                self.new_post = thread
                break
        print(self.time(), f'新帖子: {self.new_post}', flush=True)

    # 获取帖子全文（磁力、文件名、标题、封面）
    def getPostContent(self, url):
        r = requests.get(url, headers=self.header)
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find('h1', {'class': "ts"}).text.strip().replace('\n', ' ')
        post = soup.find('div', {'id': re.compile(r"post_\d*?")}).find('div', {'class': 't_fsz'})
        magnet = re.search(r'(magnet:\?xt=urn:btih:[0-9a-fA-F]{40})', post.text).group(1)
        print(magnet)
        name = re.search(r'(.+-C).torrent', post.text).group(1)
        print(name)
        img = post.table.find('img')
        if 'http' in img['file']:
            poster = img['file']
        else:
            poster = self.url + img['file']
        print(self.time(), title, "已获取", flush=True)
        return title, magnet, name, poster

    def time(self):
        strftime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return strftime

    def updateList(self):
        with open('old_posts.json', 'w') as f:
            self.old_posts.append(self.new_post)
            f.write(str(self.old_posts))
        print(self.time(), '列表已更新', flush=True)

if __name__ == '__main__':
    se = sehuatang()
    se.getNewPost()
    url = se.url + se.new_post
    title, magnet, name, poster = se.getPostContent(url)
    with open('info/url.txt', 'w') as f:
        f.write(magnet)
    with open('info/name.txt', 'w') as f:
        f.write(name)
    with open('info/poster.txt', 'w') as f:
        f.write(poster)
    with open('info/title.txt', 'w') as f:
        f.write(title)
    se.updateList()