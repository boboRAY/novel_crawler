from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool
import urllib
from tqdm import tqdm
import os
import multiprocessing
import time

root_urls = []
output_dir = './novels/'
current_title = ''


if not os.path.exists(output_dir):
    os.mkdir(output_dir)



def get_information(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    chapter_urls = [urllib.parse.urljoin(url, a['href']) for a in soup.select('.chapterlist a')]
    title = soup.select_one('.ksq_0 h1').text
    global current_title
    current_title = title
    print('now download ', title)
    return title, chapter_urls


def get_chapter(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    title = soup.h1.text.strip()

    article = soup.select('.ReadContents')[0].text
    article = article.replace('=波=斯=小=說=網= bsxsw.com', '')

    article = title + '\n' + article + '====== 本章結束 ======\n\n\n'
    return article


def crawl(url):
    title, chapter_urls = get_information(url)
    articles = []
    # with Pool(processes=4) as pool:
    #     art    result = []
    pool = Pool(4)
    for article in tqdm(pool.imap(get_chapter, chapter_urls), total=len(chapter_urls)):
        articles.append(article)
    pool.close()
    pool.join()
    global current_title
    with open(os.path.join(output_dir, current_title+'.txt'), 'w') as f:
        f.write('\n'.join(articles))


if __name__ == '__main__':
    while True:
        url = input('(input "go" to begin the process)input root url: ')
        if url == 'go':
            break
        root_urls.append(url)
    for url in root_urls:
        crawl(url)
