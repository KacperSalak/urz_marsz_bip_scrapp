from bs4 import BeautifulSoup
import globals
import regex as re
import selenium as se
import time

def print_umw_site():
    um_slownik_all = globals.UM_SITES_DICT()
    url = um_slownik_all.get("Urząd Marszałkowski Województwa Łódzkiego")
    # umw_lubel_site = requests.get(url, verify=False)    
    driver = globals.get_selen_driver()
    driver.get(url)
    time.sleep(3)
    
    
    umw_site = driver.page_source
    driver.close()
    return umw_site

def umw_site_news(site):
    soup = BeautifulSoup(site, "html.parser")
    
    news_link_sect = soup.find("a", string="Ogłoszenia")
    # news_link = news_link_sect.find("a")["href"]
    news_link = news_link_sect["href"]

    url = "https://bip.lodzkie.pl" + news_link
    # url = news_link_sect
  
    return url

def site_news_all(base_url):
    from selenium.webdriver.common.by import By
    
    news_records = []
    all_records_dict = {}
    news_urls_list = []
    range_pg = range(1, 30, 10)
    
    driver = globals.get_selen_driver()
    
    for r in range_pg:
        driver.get(f"{base_url}?start={str(r)}")
        time.sleep(3)
        
        news_lodz_site = driver.page_source

        # driver.close()

        soup_lodz_news = BeautifulSoup(news_lodz_site, "html.parser")

        lodz_news_all = soup_lodz_news.find("div", id="itemListPrimary") 
        lodz_news_link_all = lodz_news_all.find_all(class_="itemContainer itemContainerLast")

        for l in lodz_news_link_all:
            news_urls_list.append("https://bip.lodzkie.pl" + l.find("a")["href"])
    
    # driver.close()
    # return news_urls_list

    for url in news_urls_list:
        driver.get(url)
        time.sleep(2)

        stronka = driver.page_source

        news_site_soup = BeautifulSoup(stronka, "html.parser")

        try:
            news_title = news_site_soup.find("div", class_="itemHeader").text
        except:
            pass

        try:
            news_text = news_site_soup.find("div", class_="itemFullText").text
        except:
            pass

        try:
            dates = news_site_soup.find_all("div", class_="itemDateModified")
            creation_date = dates[0].text
            # creation_date = re.findall('(?<=Data publikacji: ).*(?= -)', creation_date)[0]
            creation_date = globals.clean_str_unicode(creation_date) 
            creation_date = re.findall('(?<=Data publikacji: ).*(?= -)', creation_date)[0]
        except:
            creation_date = "tu jest jakis blad"

        try:
            dates = news_site_soup.find_all("div", class_="itemDateModified")
            mod_date = dates[1].text 
            mod_date = globals.clean_str_unicode(mod_date) 
            mod_date = re.findall('(?<=Ostatnio zmieniany:).*(?= -)', mod_date)[0]
        except:
            mod_date = ""

        try:
            zalaczniki_text = []
            zalaczniki_sect = news_site_soup.find("ul", class_="itemAttachments").find_all("a")
            for z in zalaczniki_sect:
                zalaczniki_text.append(z.text)
        except:
            zalaczniki_text = []

        try:
            zalaczniki_linki = []
            zalaczniki_sect = news_site_soup.find("ul", class_="itemAttachments").find_all("a")
            for z in zalaczniki_sect:
                zalaczniki_linki.append("https://bip.lodzkie.pl" + z["href"])
        except:
            zalaczniki_linki = []

        try:
            views_count = news_site_soup.find("span", class_="itemHits").find("b").text
        except:
            views_count = "brak"
        
        news_record = {
                "url": url, 
                "tytul": news_title, 
                "tresc": news_text, 
                "zalaczniki_lista": zalaczniki_text,
                "zalaczniki_linki": zalaczniki_linki,
                "data_pub": creation_date,
                "data_mod": mod_date,
                "liczba_odslon": views_count
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