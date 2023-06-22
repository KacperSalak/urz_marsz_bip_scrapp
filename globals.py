import os.path

import requests 
from bs4 import BeautifulSoup

import selenium as se 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import regex as re
import pprint

def UM_SITES_DICT():
    um_lista_url = "https://www.bip.gov.pl/subjects/index/6198"
    um_lista_page = requests.get(um_lista_url)

    soup = BeautifulSoup(um_lista_page.content, "html.parser")
    result_url = soup.find(id="content")

    links_unpar = result_url.find("ul", class_="subjects").find_all("a")

    adresy=[]
    um_slownik={}

    um_nazwy = [tagi.text.strip() for tagi in links_unpar]

    for tagi in links_unpar:
        link = tagi["href"]
        adresy.append(f"https://bip.gov.pl{link}")
    
    for i in range(len(um_nazwy)):
        um_slownik[um_nazwy[i]] = adresy[i]

    for key, value in um_slownik.items():
        sub_s = requests.get(value)
        sub_s_result = BeautifulSoup(sub_s.content, "html.parser")
        try:
            sub_s_parsed = sub_s_result.find("h2").find("a")
        # sub_s_parsed = sub_s_result.find("h2")
            um_slownik[key] = sub_s_parsed["href"]
        except:
            sub_s_parsed = "BRAK DANYCH"
            um_slownik[key] = sub_s_parsed

    return um_slownik
    # return sub_s_result

print(UM_SITES_DICT())

def clean_str_unicode(str_text):
    str_text = str_text.replace(u"\xa0", u"")
    str_text = str_text.replace(u"\n", u"")
    str_text = str_text.replace(u"\r", u"")
    str_text = str_text.replace(u"\t", u"")
    str_text = re.sub("[?<=\s][?=\s]", "", str_text)

    return str_text

def get_selen_driver():

    opt = webdriver.ChromeOptions()
    opt.add_argument("--no-sandbox")
    opt.add_argument("--headless=new")

    homedir = os.path.expanduser("~")
    webdriver_service = Service(f"{homedir}/driver/stable/chromedriver")

    driver = webdriver.Chrome(service = webdriver_service, options=opt)
    
    return driver
