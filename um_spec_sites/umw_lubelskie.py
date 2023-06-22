import requests
from bs4 import BeautifulSoup
import globals
import regex as re


def print_umw_site():
    um_slownik_all = globals.UM_SITES_DICT()
    url = um_slownik_all.get("Urząd Marszałkowski Województwa Lubelskiego")
    umw_lubel_site = requests.get(url, verify=False)    
    return umw_lubel_site

def umw_site_news(site):
    soup_lubel = BeautifulSoup(site.content, "html.parser")
    
    news_link_all = soup_lubel.find_all("a", string="Aktualności")
    news_link = ""
    for a in news_link_all:
        if a["href"] == "/index.php?id=88":
            news_link += str(a["href"])
            break

    url = "https://umwl.bip.lubelskie.pl" + news_link
  
    return url

def site_news_all(base_url):

    import time
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    # range_pg = range(1, 6)
    
    news_urls_list = []
    news_records = []
    all_records_dict = {}
    

    driver = globals.get_selen_driver()
    driver.get(base_url)

    select_opt = driver.find_element(By.XPATH, "//select[@class='text-center form-control form-control-sm']")

    select = Select(select_opt)
    select.select_by_value('1000')
    
    try:
        WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located((By.XPATH, "//tbody/*")))
    except TimeoutException:
        pass

    news_lubel_site = driver.page_source
    time.sleep(3)

    driver.close()
    soup_lubel_news = BeautifulSoup(news_lubel_site, "html.parser")
    
    komms = soup_lubel_news.find("tbody")
    for k in komms.find_all("a", href=True):
        news_urls_list.append("https://umwl.bip.lubelskie.pl/index.php"+ k["href"])


    for komm in news_urls_list[:25]:
        stronka = requests.get(komm)
        stronka = BeautifulSoup(stronka.content, 'html.parser')

        try:
            # news_all = stronka.find_all("div", class_="col-md-9 text-bold")
            news_all = stronka.find_all("div", class_="row mb-4 align-items-center")
            zalacz_all = stronka.find("div", class_="row mb-4")      
            print(news_all)
            try:
                news_title = globals.clean_str_unicode(news_all[0].text)
                news_title = re.findall('(?<=Tytuł).*(?= )', news_title)[0]
            except:
                pass

            try:
                creation_date = globals.clean_str_unicode(news_all[1].text)
                creation_date = re.findall('(?<=Data utworzenia).*(?=)', creation_date)[0]
            except:
                pass

            try:
                news_text = []
                # news_text_html = news_all.find("div", class_="col-md-9")
                try:
                    for n in news_all[3].find_all(["p", "li"]):
                        news_text.append(n.text)
                    # print(news_text_html)
                except:
                    for n in news_all[2].find_all(["p", "li"]):
                        news_text.append(n.text)                    
                    pass
                news_text = " ".join(news_text)
                news_text = globals.clean_str_unicode(news_text)
                # news_text = news_all[3].text
            except:
                news_text = []

            try:
                zalacz_text = []
                zalacz_files = []
                zalaczniki = zalacz_all.find_all(class_="file-details d-flex flex-wrap flex-md-nowrap mb-3")

                for z in zalaczniki:
                    try:
                        zalacznik = z.find("a")
                        zalacz_text.append(zalacznik.text)
                    except:
                        zalacz_text = []
                    try:
                        zalacznik_link = z.find("a")["href"]
                        zalacz_files.append("https://umwl.bip.lubelskie.pl/" + zalacznik_link)
                    except:
                        zalacz_files = []
            except:
                # zalacz_ = []
                # zalacz_files = []
                pass

            news_record = {
                "url": komm,
                "tytul": news_title,
                "tresc": news_text,
                "zalaczniki": zalacz_text,
                "zalaczniki_linki": zalacz_files,
                "data_pub": creation_date
                }
        except:
            # news_record = {}
            pass
        news_records.append(news_record)

    for i in range(len(news_urls_list[:25])):
        all_records_dict[i] = news_records[i]

    return all_records_dict
    # print(all_records_dict)

    