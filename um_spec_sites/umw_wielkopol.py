from bs4 import BeautifulSoup
import globals
import regex as re
import time

def print_umw_site():
    um_slownik_all = globals.UM_SITES_DICT()
    url = um_slownik_all.get("Urząd Marszałkowski Województwa Wielkopolskiego")

    driver = globals.get_selen_driver()
    driver.get(url)
    time.sleep(3)

    umw_site = driver.page_source
    driver.close()

    return umw_site


def umw_site_news(site):
    soup = BeautifulSoup(site, "html.parser")
    
    news_link_sect = soup.find("a", string="Ogłoszenia ")
    # news_link = news_link_sect.find("a")["href"]
    news_link = news_link_sect["href"]

    url = "https://bip.umww.pl/" + news_link

    driver = globals.get_selen_driver()
    driver.get(url)

    news_latest = driver.page_source
    soup = BeautifulSoup(news_latest, "html.parser")
    
    # news_link_archiv_sect = soup.find("a", string=" Ogłoszenia - archiwum ")
    news_link_archiv_sect = soup.find_all("div", class_="news")[-1]
    
    news_link = news_link_archiv_sect.find("a")["href"]

    url = "https://bip.umww.pl/" + news_link

    driver.get(url)
    news_archive = driver.page_source

    soup = BeautifulSoup(news_archive, "html.parser")

    all_archives = soup.find_all("div", class_="news")
    all_years_news_url = []
    
    for a in all_archives:
        if re.fullmatch(".*--(201[0-6])", a.find("a")["href"]):
            all_years_news_url.append("https://bip.umww.pl/" + a.find("a")["href"])
        elif re.fullmatch(".*--(2017|2020)", a.find("a")["href"]):
            for i in range(1, 3):
                all_years_news_url.append(f"https://bip.umww.pl/index.php?page={i}&ipp=30&zm1=" + a.find("a")["href"])
        else:
            for i in range(1, 4):
                all_years_news_url.append(f"https://bip.umww.pl/index.php?page={i}&ipp=30&zm1=" + a.find("a")["href"])

    driver.close()
  
    return all_years_news_url

def site_news_all(base_url_list):
    from selenium.webdriver.common.by import By
    
    news_records = []
    all_records_dict = {}
    news_urls_list = []

    driver = globals.get_selen_driver()
    
    for strona in base_url_list:
        driver.get(strona)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        komm_all = soup.find("div", id="artykul").find_all("div", class_="news")

        for k in komm_all:
            news_urls_list.append("https://bip.umww.pl/" + k.find("a")["href"])

    for url in news_urls_list:
        driver.get(url)
        time.sleep(2)

        stronka = driver.page_source

        news_site_soup = BeautifulSoup(stronka, "html.parser")

        try:
            news_title = news_site_soup.find("div", id="tresc-drukuj").find("h1").text
        except:
            news_title = ""

        try:
            news_text = [n.text for n in news_site_soup.find("div", id="tresc-drukuj").find_all(["p", "li"])]
            news_text = " ".join(news_text)
        except:
            news_text = ""

        try:
            dates = news_site_soup.find("div", id="podpis_autor_lewa")
            # creation_date = dates.find("br", string=re.match("(wytworzenie informacji:).*")).text
            # creation_date = dates.find(lambda tag: tag.name == "br" and "wytworzenie informacji:" in tag.text).text
            # creation_date = re.findall('(?<=Data publikacji: ).*(?= -)', creation_date)[0]
            creation_date = dates.find_all(["strong","span"])
            creation_date = globals.clean_str_unicode(creation_date[2].text) 
        except:
            creation_date = ""
        
        try:
            dates = news_site_soup.find("div", id="podpis_autor_lewa")
            mod_date = dates.find_all(["strong","span"])
            mod_date = globals.clean_str_unicode(mod_date[4].text)
        except:
            mod_date = ""

        news_record = {
                "url": url, 
                "tytul": news_title, 
                "tresc": news_text, 
                # "zalaczniki_lista": zalaczniki_text,
                # "zalaczniki_linki": zalaczniki_linki,
                "data_pub": creation_date,
                "data_mod": mod_date
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