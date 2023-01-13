import concurrent.futures
from lxml.html import fromstring
import Scraper #


Collin_url_1 = "https://www.collincad.org/propertysearch?prop_id="
Collin_url_2 = "&situs_street_suffix=&isd%5B%5D=any&city%5B%5D=any&prop_type%5B%5D=R&prop_type%5B%5D=P&prop_type%5B%5D=MH&active%5B%5D=1&year=2022&sort=G"


file = open("new_data_Collin.csv", 'r').readlines()


headers = {


    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.9",
    "Host": "httpbin.org",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    "X-Amzn-Trace-Id": "Root=1-63baa1f0-7fd6092b70f6532741e1d6bb"


}
### From csv file of ~500000 rows I got the IDs of Collin County to put into the main link to access pages needed to be scraped, then I've written it into an another csv file to make it faster to load during writting and debugging the scraper


"""file = open("City_Of_Dallas_Parcel_IDs.csv", "r").readlines()
splitted_file = []
data = {"Dallas": [], "Kaufman": [], "Denton": [], "Collin": [], "Rockwall": []}
for i in file:
    splitted_file.append(i.split(";"))
for record in splitted_file[1:]:
    if record[3] == "Dallas":
        data["Dallas"].append(record[1])
    elif record[3] == "Denton":
        data["Denton"].append(record[1])
    elif record[3] == "Collin":
        data["Collin"].append(record[1])
    elif record[3] == "Kaufman":
        data["Kaufman"].append(record[1])
    else:
        data["Rockwall"].append(record[1])

new_file_Collin = open("new_data_Collin.csv","a")
for j in data["Collin"]:
    new_file_Collin.writelines(j[4:]+";"+"\n")
"""


scraper = Scraper
new_file_Collin = open("new_data_Collin.csv", "r").readlines()
final_data_Collin = open("final_data_Collin1.csv", "a")





def get_Collin(link):
    body = scraper.download(link)

    tree = fromstring(body.html)
    td = tree.xpath('//div[@class="propertyinfo_container"]/div[@class ="propertyinfo"]/dl /dt')
    headers= []
    for index1 in td:
        info1 = index1.text_content()
        headers.append(info1)

    td2 = tree.xpath('//div[@class="propertyinfo_container"]/div[@class ="propertyinfo"]/dl /dd')
    data = []
    for index2 in td2:
        info2 = index2.text_content()
        data.append(info2)

crawl_queue = []

for parcelID in new_file_Collin:
    crawl_queue.append(Collin_url_1 + parcelID[:-2] + Collin_url_2)
with concurrent.futures.ThreadPoolExecutor() as executor: # I used concurent futures module to make the scraper work a lot faster
    executor.map(get_Collin, crawl_queue)


