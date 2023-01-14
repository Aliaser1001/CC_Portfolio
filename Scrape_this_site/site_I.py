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
    scraped_data = []
    html = download(url)
    tree = fromstring(html)
    country_names = tree.xpath('//div[@class="row"]/div[@class="col-md-4 country"]/h3')[3:-1]
    td = tree.xpath('//div[@class="row"]/div[@class="col-md-4 country"]/div')[3:-1]
    for i in range(len(td)):
        info = td[i].text_content()
        scraped_data.append(country_names[i].text_content().strip()+';'+ info.strip().replace("\n                            ",';'))
    return scraped_data

def write2file(Table, type):
    with open(f'result.{type}', 'a') as file:
        for row in Table:
            file.write(row+'\n')
    file.close()
if __name__ == '__main__':
    data = scrape(url)
    write2file(data, 'csv')