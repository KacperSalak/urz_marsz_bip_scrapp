import requests
from bs4 import BeautifulSoup
import globals
import regex as re
import time

def print_umw_site():
    um_slownik_all = globals.UM_SITES_DICT()
    url = um_slownik_all.get("Urząd Marszałkowski Województwa Dolnośląskiego")
    if re.match("(http:\/\/www\.).*", url):
        url = url.replace(r"http://www.",r"https://")
    # umw_dslask_site = requests.get(url, verify=False)
    driver = globals.get_selen_driver()
    
    driver.get(url)
    time.sleep(5)

    umw_dslask_site =  driver.page_source
    driver.close()

    return umw_dslask_site

def umw_site_news(site):
    # site = site + r"/"
    soup_maz = BeautifulSoup(site, "html.parser")

    news_link = soup_maz.find("a", string="Aktualności i Ogłoszenia")
    news_link=news_link["href"] 

    url = "https://bip.dolnyslask.pl" + news_link

    return url

def site_news_all(base_url):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support import expected_conditions as EC

    news_records = []
    all_records_dict = {}
    
    # from selenium.webdriver.chrome.options import Options
    range_pg = range(1, 47)
    driver = globals.get_selen_driver()

    for pg_num in range_pg:
        driver.get(base_url + "?page=" + str(pg_num))    
        # driver.get(f"{base_url}?page={str(pg_num)}")
        time.sleep(3)
        
        try:
            WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located((By.XPATH, "//td[@class='sc-pAkoP fNcScZ']")))
            url = driver.page_source
        except TimeoutException:
            pass

        soup_dolny_news = BeautifulSoup(url, "html.parser")
        # test1 = soup_dolny_news.find("div", class_="sc-fzqKVi dniAa")
        # komms = soup_dolny_news.find_all("tr", class_="sc-qXTOB dVNqbi")
        komms = soup_dolny_news.find_all("tr")
        for k in komms:
            title = k.find(class_="sc-pAkoP fNcScZ")
            data_pub = k.find(class_="sc-pAkoP iqlssu")
            try:
                title = re.findall('(?<="sc-pAkoP fNcScZ"\>).*(?=\<\/td\>)', str(title))[0]
                # news_urls_list.append(title)
            except:
                pass

            try:
                data_pub = re.findall('(?<="sc-pAkoP iqlssu"\>).*(?=\<\/td\>)', str(data_pub))[0]
            except:
                pass

            news_record = {
                "tytul": title,
                "data_pub": data_pub,
                }
            
            news_records.append(news_record)
    
    for i in range(len(news_records)):
        all_records_dict[i] = news_records[i]
            # data_pub = k.find()
        # WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "a")))

        # url = driver.page_source

        # soup_dolny_news = BeautifulSoup(url, "html.parser")
        # # test1 = soup_dolny_news.find("div", class_="sc-fzqKVi dniAa")
        # # komms = soup_dolny_news.find_all("tr", class_="sc-qXTOB dVNqbi")
        # komms = soup_dolny_news.find_all("tbody")
        # for k in komms:
        #     k = k.find("a")
        #     news_urls_list.append(k["href"])
        #     news_urls_list.append(k)
    
    driver.close()

    return all_records_dict



