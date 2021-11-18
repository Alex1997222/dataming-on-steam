import re
import socket
import urllib
import urllib.request
from contextlib import closing
from time import sleep

def download_page(url, maxretries, timeout, pause):
    tries = 0
    htmlpage = None
    while tries < maxretries and htmlpage is None:
        try:
            with closing(urllib.request.urlopen(url, timeout=timeout)) as f:
                htmlpage = f.read()
                sleep(pause)
        except (urllib.error.URLError, socket.timeout, socket.error):
            tries += 1
    return htmlpage

def getGameList(timeout=180, maxretries=3, pause=1):
    baseurl = 'http://store.steampowered.com/search/results?sort_by=_ASC&snr=1_7_7_230_7&page='
    page = 0
    gameidre = re.compile(r'/(app|sub)/([0-9]+)/')

    retries = 0
    while True:
        url = '%s%s' % (baseurl, page)
        print(page, url)
        htmlpage = download_page(url, maxretries, timeout, pause)

        if htmlpage is None:
            print('Error downloading the URL: ' + url)
            sleep(pause * 10)
        else:
            htmlpage = htmlpage.decode()
            with open(os.path.join(pagedir, 'games-page-%s.html' % page), mode='w', encoding='utf-8') as f:
                f.write(htmlpage)

            pageids = set(gameidre.findall(htmlpage))
            if len(pageids) == 0:
                # sometimes you get an empty page but it is not actually
                # the last one, so it is better to retry a few times before
                # considering the work done
                if retries < maxretries:
                    print('empty page', retries)
                    sleep(5)
                    retries += 1
                    continue
                else:
                    break
            print(len(pageids), pageids)
            retries = 0
            page += 1
