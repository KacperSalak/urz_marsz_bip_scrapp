from bs4 import BeautifulSoup
import globals
import regex as re
import selenium as se
import time

def print_umw_site():
    um_slownik_all = globals.UM_SITES_DICT()
    url = um_slownik_all.get("Urząd Marszałkowski Województwa Podlaskiego")

    url = url + "strona_glowna_bip.html"
    
    return url

def site_news_all(base_url):
    from selenium.webdriver.common.by import By
    
    news_records = []
    all_records_dict = {}
    news_urls_list = []
    range_pg = range(1, 4)
    
    driver = globals.get_selen_driver()
    
    for r in range_pg:
        driver.get(f"{base_url}?page={str(r)}")
        time.sleep(3)

        news_site = driver.page_source

        soup_news = BeautifulSoup(news_site, "html.parser")

        news_all = soup_news.find("ul", class_="list") 
        news_link_all = news_all.find_all(class_="component-item clearfix")

        for l in news_link_all:
            news_urls_list.append("https://bip.wrotapodlasia.pl" + l.find("a")["href"])

    for url in news_urls_list:
        driver.get(url)
        time.sleep(2)

        stronka = driver.page_source

        news_site_soup = BeautifulSoup(stronka, "html.parser")

        try:
            news_title = news_site_soup.find("div", class_="component-title component-page-title").text
        except:
            pass

        try:
            news_text = news_site_soup.find("div", {"data-name":"Cms_ContentWYSIWYG"}).text
        except:
            news_text = ""
        
        try:
            news_attach_names = []
            news_attach = news_site_soup.find("div", {"data-name":"Cms_Attachment"}).find_all("div", class_="attachment-item")
            for n in news_attach:
                attach_name = n.find("a").text
                news_attach_names.append(attach_name)
        except:
            news_attach_names = []

        try:
            news_attach_links = []
            news_attach = news_site_soup.find("div", {"data-name":"Cms_Attachment"}).find_all("div", class_="attachment-item")
            for n in news_attach:
                attach_link = n.find("a")["href"]
                news_attach_links.append("https://bip.wrotapodlasia.pl" + attach_link)
        except:
            news_attach_links = []
        
        metric = news_site_soup.find_all("p", class_="component-info-params")
        
        try:
            creation_date = metric[-1].find("span").text
        except:
            creation_date = "tu jest błąd"

        try:
            mod_date = metric[-3].find("span").text
        except:
            mod_date = "tu jest błąd"

        try:
            publisher = metric[0].find("span").text
        except:
            publisher = "tu jest błąd"


        news_record = {
                "url": url, 
                "tytul": news_title, 
                "tresc": news_text, 
                "zalaczniki_lista": news_attach_names,
                "zalaczniki_linki": news_attach_links,
                "data_pub": creation_date,
                "data_mod": mod_date,
                "udostepnia" : publisher
                }
        
        for key, value in news_record.items():
            try:
                news_record[key] = globals.clean_str_unicode(value)
            except:
                pass

        news_records.append(news_record)
    
    driver.close()

    for i in range(len(news_urls_list)):
        all_records_dict[i] = news_records[i]

    return all_records_dict