import requests
from lxml.html import fromstring
from urllib import robotparser
url = 'https://www.scrapethissite.com/pages/simple/'
def robots(url):
    rp = robotparser.RobotFileParser()
    rp.set_url(url)
    rp.read()
    return rp
def download(url, num_retries=3):
    print('Downloading the url:', url)
    headers = {'User-Agent':'cc'}
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        if response.status_code >= 400:
            print('Download error:', response.text)
            if num_retries> 0 and 500 <= response.status_code<=600:
                return download(url, num_retries=num_retries-1)
    except requests.exceptions.RequestException as e:
        print(e.reason)
        html = None
    return html

def scrape(url):
    html = download(url)
    tree = fromstring(html)
    td = tree.xpath('//div[@class="row"]')[3:-1]
    for i in td:
        info = i.text_content().strip()
        print(info)

print(scrape(url))
