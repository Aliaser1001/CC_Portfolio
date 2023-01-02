from urllib.parse import urljoin
from urllib.error import URLError, HTTPError, ContentTooShortError
from urllib import robotparser
import urllib.request
import re
import Throttle
from lxml.html import fromstring, tostring
import cssselect

url = "https://webscraper.io/test-sites/e-commerce/allinone"
r_url = "https://webscraper.io/robots.txt"
# Because the page was bigger than the example e-commerce shop I have manually written "robots.txt" url
user_agent = "cc"


def get_robots_parser(robots_url):
    # But if we start with normal site, then this function will read the "robots.txt" file
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp


def download(url, user_agent="cc", num_retries=2, charset='utf-8'):
    print("Downloading the:", url)
    request = urllib.request.Request(url)
    request.add_header('User_agent', user_agent)
    # Trying to open and download the html file
    try:
        resp = urllib.request.urlopen(request)
        cs = resp.headers.get_content_charset()
        if not cs:
            cs = charset
        html = resp.read().decode(cs)
    except (URLError, HTTPError, ContentTooShortError) as e:
        print("Download error:", e.reason)
        html = None
        if num_retries > 0:
            # Checking if the problem is with the client or something else and recursively downloading the html file
            if hasattr(e, "code") and 500 <= e.code <= 600:
                return download(url, num_retries - 1)

    return html


def get_links(html):
    # This function gets all the important links from crawled web page using regex
    webpage_regex = re.compile("""<a[^>]+href=["'](/test-sites/e-commerce/allinone.*?)["']""", re.IGNORECASE)
    return webpage_regex.findall(html)


def write2csv(A):
    file = open("data.csv", "a")
    file.write(";"+str(A))
    file.close()


def link_crawler(start_url, robots_url, delay, user_agent="cc", max_depth=5):
    # Creating the object of Throttle class to implement cooldown between each download
    throttle = Throttle.Throttle(delay)
    crawl_queue = [start_url]
    seen = {}
    """if not robots_url:
        robots_url = "{}/robots.txt".format(start_url)"""
    rp = get_robots_parser(robots_url)
    while crawl_queue:
        url = crawl_queue.pop()
        if rp.can_fetch(user_agent, url):
            depth = seen.get(url,0)
            if depth == max_depth:
                # In case of spider traps
                print('Skipping %s due to depth' % url)
                continue
            throttle.wait(url)
            html = download(url, user_agent=user_agent)
            if not html:
                # Checking if the current url provides something
                continue
            if "/product/" in url:
                # Writing to .csv file description from product's site
                write2csv(url)
                tree = fromstring(html)
                td = tree.cssselect('.caption')[0]
                for index in td:
                    info = index.text_content()
                    write2csv(str(info))
                write2csv("\n")
            for link in get_links(html):
                # Creates the next link to crawl
                abs_link = urljoin(start_url, link)
                if abs_link not in seen:
                    seen[abs_link] = depth+1
                    crawl_queue.append(abs_link)
        else:
            print("Blocked by robots.txt:", url)


link_crawler(url, r_url, 1)
