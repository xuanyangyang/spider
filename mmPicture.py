import urllib.request
import os
import random
import re
import urllib.error
from iplist import Iplist

iplist = Iplist('http://www.xicidaili.com/nt/').get_ip_list()
current_ip = '0'


def change_proxy():
    global iplist
    if len(iplist) == 0:
        print('更新列表')
        iplist = Iplist('http://www.xicidaili.com/nt/').get_ip_list()
    proxy = random.choice(iplist)
    global current_ip
    current_ip = proxy
    print('使用' + proxy)
    proxy_support = urllib.request.ProxyHandler({'http': proxy})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)

def open_url(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent',
                   "Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4")

    try:
        response = urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print(e.reason)
        elif hasattr(e, 'code'):
            print(e.code)
        if current_ip != '0':
            print('丢弃' + current_ip)
            iplist.remove(current_ip)
        change_proxy()
        html = open_url(url)
        return html
    else:
        html = response.read()
        return html


def get_page(url):
    html = open_url(url).decode('utf-8')

    page = re.findall('<span class="current-comment-page">\[(\d\d\d\d)\]</span>', html)[0]
    page = int(page)

    return page


def find_img(url):
    html = open_url(url).decode('utf-8')

    imgs = re.findall('<img src="(.*jpg)" />', html)

    return imgs


def save_img(imgs):
    for img in imgs:
        print('图片地址：'+img)
        imgName = img.split('/')[-1]
        with open(imgName, 'wb') as f:
            f.write(open_url(img))


def download_mm(folder='MM'):
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)

    url = 'http://jandan.net/ooxx/'

    page = get_page(url)

    for i in range(page, 1, -1):
        page_url = url + 'page-' + str(i) + '#comments'
        print(page_url)
        imgs = find_img(page_url)
        save_img(imgs)

if __name__ == '__main__':
    download_mm()
