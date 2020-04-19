from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import bs4
import pandas as pd

sites = pd.read_csv('Data\Websites.csv', header = None)
sites.columns = ['Hotel', 'URL']
print(sites)

#Use Chrome browser to read data from the above list of Restaurant URLs.
options = Options()
options.headless = True
EXE_PATH = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'

## This part does infinite scorlling.
def get_reviews(hotel, url1):
    print(hotel, url1)
    driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=options)
    driver.get(url1)
    time.sleep(5)
    driver.find_element_by_xpath("//*[contains(text(), 'All Reviews')]").click()
    time.sleep(5)
    load = 0
    while 1==1:
        try:
            l = driver.find_element_by_xpath("//*[contains(text(), 'Load More')]")
        except:
            break
        if l:
            load += 1
            l.click()
            time.sleep(5)
            #r = driver.find_element_by_xpath("//*[contains(text(), 'read more')]")
        else:
            break
    print(load)
    html=driver.page_source
#html = driver.execute_script("return document.body.innerHTML;")
    file_name = 'Data\\' + hotel + '.html'
    f=open(file_name, "wb", )
    f.write(html.encode("utf-8"))
    f.close()
    driver.close()

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def gen_csv(hotel):
    file_name = 'Data\\' + hotel + '.html'
    csv_name = 'Data\\' + hotel + '.csv'
    f = open(file_name, "rb")
    html = f.read().decode("utf-8")
    f.close()
    soup = bs4.BeautifulSoup(html, "html.parser")
    rev = []
    for e in soup.find_all("div", class_="rev-text"):
        rev.append(strip_non_ascii(e.text))

    ratings = []
    for e in soup.find_all("div", class_="rev-text"):
        if e.div.get('aria-label') is not None:
            ratings.append(e.div.get('aria-label'))
        else:
            ratings.append('Rated 0')

    ratings_cleaned = list(map(lambda x: x.replace("Rated", "").strip(), ratings))

    reviews_cleaned = list(map(lambda x: x.replace("Rated", "").strip(), rev))
    reviews_cleaned = list(map(lambda x: x.replace("\r\n", " ").strip(), reviews_cleaned))
    reviews_cleaned = list(map(lambda x: x.replace("\n", " ").strip(), reviews_cleaned))

    ratings_df = pd.DataFrame({"Rating": ratings_cleaned, "Review": reviews_cleaned})
    ratings_df.Review = ratings_df.Review.map(lambda x: x.strip())
    ratings_df.to_csv(csv_name, index=False, encoding="utf-8")

for i in range(len(sites)):
    print(i)
    driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=options)
    get_reviews(sites.iloc[i,0], sites.iloc[i,1])
    gen_csv(sites.iloc[i,0])