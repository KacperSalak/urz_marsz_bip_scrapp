import requests
from bs4 import BeautifulSoup
import globals
import regex as re


def print_umw_site():
    um_slownik_all = globals.UM_SITES_DICT()
    url = um_slownik_all.get("Urząd Marszałkowski Województwa Mazowieckiego")
    umw_mazow_site = requests.get(url, verify=False)    
    return umw_mazow_site

def umw_site_news(site):
    soup_maz = BeautifulSoup(site.content, "html.parser")
    
    news_link_sect = soup_maz.find("div", {"data-section_name": "Komunikaty"})
    news_link = news_link_sect.find("a")["href"]

    url = "https://bip.mazovia.pl" + news_link
  
    return url

def site_news_all(base_url):
    range_pg = range(1, 76)
    news_urls_list = []
    news_records = []
    all_records_dict = {}
    
    
    for pg_num in range_pg:
        news_maz_site=requests.get(base_url + "/komunikaty.html?page=" + str(pg_num))
        soup_maz_news = BeautifulSoup(news_maz_site.content, "html.parser")
                    
        komms = soup_maz_news.find("ul", class_="list")
        for k in komms.find_all("a", href=True):
            news_urls_list.append("https://bip.mazovia.pl"+ k["href"])

    driver = globals.get_selen_driver()

    for url in news_urls_list:
        news_record = {}
        # news = requests.get(url)
        driver.get(url)
        news = driver.page_source
        soup_news = BeautifulSoup(news, "html.parser")
        try:
            news_title = soup_news.find("h1").text 

            news_subtitle = soup_news.find("div", class_= "component-description item").find("p").text

            news_html = soup_news.find("div", class_="component-main-content component-content-wysiwyg item").find_all(["p", "li"])
            news_text = []
            for n in news_html:
                news_text.append(n.text)
            news_text = " ".join(news_text)
            news_text = globals.clean_str_unicode(news_text)

            
            news_files_names=[]
            try:
                news_files = soup_news.find("ul", class_="list-attachment").find_all("li")
                for zal in news_files:
                    zal = zal.find("a")
                    news_files_names.append(zal.text)
            except:
                pass
            
            news_metric = soup_news.find("div", class_="row component-content bit-expand-area").find_all("p")
            try:
                news_public_agent = str(news_metric[0].text)
                news_public_agent = news_public_agent.replace("Podmiot udostępniający: ", "")
            except:
                pass
            
            try:
                pub_dttm = str(news_metric[4].text)
                pub_dttm = re.findall('(?<=Data opublikowania: ).*(?= )', pub_dttm)[0]
            except:
                pass

            try:
                mod_dttm = str(news_metric[6].text)
                mod_dttm = re.findall('(?<=Data ostatniej aktualizacji: ).*(?= )', mod_dttm)[0]
            except:
                pass

            try:
                views_count = str(news_metric[7].text)
                views_count = views_count.replace("Liczba wyświetleń: ", "")
            except:
                pass

            news_record = {
                "url": url, 
                "tytul": news_title, 
                "sub_tytul":news_subtitle, 
                "tresc": news_text, 
                "att_text": list(news_files_names),
                "public_name":news_public_agent,
                "data_pub": pub_dttm,
                "data_mod": mod_dttm,
                "view_cnt": views_count
                }
            print(news_record)
        except:
            pass
        news_records.append(news_record)

    driver.quit()
    
    for i in range(len(news_urls_list)):
        all_records_dict[i] = news_records[i]

    return all_records_dict


    
