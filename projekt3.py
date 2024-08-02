"""
projekt3.py: třetí projekt do Engeto Online Python Akademie 
author: Michal Šimek
email: simek.vys@seznam.cz
discord: smk6666
"""
import sys
import os
import requests
import csv
from bs4 import BeautifulSoup

# funkce získání rozparsovaného html zdrojového kódu
def rozparsované_html(url:str):
    soup = BeautifulSoup(requests.get(url).text, features="html.parser")
    return soup

# funkce načtení všech odkazů
def nacteni_vsech_odkazu()->tuple[list, str]:
    soup = rozparsované_html("https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ#1")
    tabulky = soup.find_all("table")
    #print(len(tabulky))
    odkazy = []
    mesta = []
    odkaz_zahranici = ""
    for a, b in enumerate(tabulky, start= 1):
        for c in b.find_all("td", {"headers":"t" + str(a) + "sa3"}):
            if  c.findPreviousSibling("td").findPreviousSibling("td").text.strip() == "Zahraničí":
                odkaz_zahranici = "https://volby.cz/pls/ps2017nss/" + c.a.attrs["href"] 
            odkazy.append(c.a.attrs["href"])
            mesta.append(c.findPreviousSibling("td").findPreviousSibling("td").text)
    #print(odkazy)
    #print(mesta)        

    odkazy_cele = ["https://volby.cz/pls/ps2017nss/" + i for i in odkazy]
    return odkazy_cele, odkaz_zahranici

#funkce ověření správnosti vstupních systémových argumentů
def overeni_vstupu(c:list):
    if len(sys.argv) != 3:
        print("Spusťte soubor se zadanými 2 argumenty v uvovovkách, oddělenými mezerou.")    
    elif  sys.argv[1] not in c:
        print("První argument není platný odkaz, spusťte soubor znovu s platným argumentem.")
    
    elif os.path.splitext(sys.argv[2])[1] != ".csv":
        print("Jméno soboru musí mít příponu .csv, spusťte program se správnou příponou.")
    else:
        try:
            a = open(sys.argv[2], mode="r")
            a.close()
            print("Soubor již existuje, spusťte program s jiným názvem souboru.")
        except FileNotFoundError:   
            try:
                b = open(sys.argv[2], mode="w")
                b.close()
                if sys.argv[2] in os.listdir(os.getcwd()):
                    print("Vše je správně.")
                    return True
                else:
                    print("Název souboru obsahuje neplatné znaky, spusťte s korektním názvem souboru.")      

            except:
                print("Název souboru obsahuje neplatné znaky, spusťte s korektním názvem souboru.")    
        except:
            print("Název souboru obsahuje neplatné znaky, spusťte s korektním názvem souboru.")

#funkce načtení všech obcí a jejich čísel
def nacteni_vsech_obci(url:str):
    """
    funkce vrací list, který obsahuje samostatný dict pro každou obec
    ze zadaného odkazu, v každém dictu jsou 3 prvky s informací o
    odkazu, čísle, názvu obce 
    """
    soup = rozparsované_html(url)
    tabulky = soup.find_all("table")
    vsechny_obce = []
    for a, b in enumerate(tabulky, start= 1):
        for c in b.find_all("td", {"headers":"t" + str(a) + "sa1 t" + str(a) + "sb1"}):
            try:
                obec = {}
                obec["odkaz"] = "https://volby.cz/pls/ps2017nss/" + c.a["href"]
                obec["Číslo"] = c.text
                obec["Obec"]= c.findNextSibling("td").text.strip()
                vsechny_obce.append(obec)
            except:
                continue
    #print(len(vsechny_obce))
    #print(vsechny_obce)
    return vsechny_obce

# funkce načtení všech zahraničních obcí
def nacteni_vsech_zahranicnich_obci(url:str):
    """
    speciální funkce pro odkaz na zahraniční obce,
    vynuceno tím, že informace pro zahraničí jsou 
    ve zdroji v jiné podobě než pro české územní celky,
    funkce vrací list dictů
    """
    soup = rozparsované_html(url)
    tabulka = soup.find("table")
    vsechny_obce = []
    for c in tabulka.find_all("td", {"headers":"s4"}):
        vsechny_obce.append({"odkaz":"https://volby.cz/pls/ps2017nss/" + c.a["href"], "Číslo":c.text,\
        "Obec":c.findPreviousSibling("td").text.strip()})
    return vsechny_obce   

#funkce načtení souhrnu
def nacteni_souhrnu(obec:dict):
    """
    funkce doplní do dictu informace ze sumární tabulky
    pro danou obec
    """
    soup = rozparsované_html(obec["odkaz"])
    tabulky = soup.find_all("table")
    for a in tabulky[0].find_all("th"):
        if a.text.strip().lower().startswith("voliči"):
            hlavicka_volici = a["id"]
        if a.text.strip().lower().startswith("vydané"):
            hlavicka_obalky = a["id"]      
        if a.text.strip().lower().startswith("platné"):
            hlavicka_hlasy = a["id"]   
    obec["Voliči"] = tabulky[0].find("td", {"headers":hlavicka_volici}).text.replace("\xa0", " ")
    obec["Obálky"] = tabulky[0].find("td", {"headers":hlavicka_obalky}).text.replace("\xa0", " ")    
    obec["Hlasy"] = tabulky[0].find("td", {"headers":hlavicka_hlasy}).text.replace("\xa0", " ")
    #print(obec)
    #print("-----------")
    return obec

#funkce načtení stran
def nacteni_stran(obec:dict):
    """
    funkce přidá do dictu politické strany a jejich získané hlasy
    """
    soup = rozparsované_html(obec["odkaz"])
    tabulky = soup.find_all("table")
    for a, b in enumerate(tabulky[1:], start=1): 
        for c in b.find_all("td", {"headers":"t" + str(a) + "sa1 t" + str(a) + "sb2"}):
            try:
                obec[c.text.strip()] = c.findNextSibling("td").text.strip().replace("\xa0", " ")
            except:
                continue
            else:
                if c.text.strip() == "-":
                    del obec[c.text.strip()]

    # print(obec)
    # print(sum([ int(a) for a in list(obec.values())[6:]]), obec["Hlasy"])
    return obec
            
def vytvoreni_hlavicky_csv(obce_strany:list)->list:
    hlavicka_csv = list(obce_strany[0].keys())[1:]
    for a in obce_strany[1:]:
        for b in list(a.keys())[1:]:
            if b not in hlavicka_csv:
                hlavicka_csv.append(b)
    #print(hlavicka_csv)
    return hlavicka_csv

def zapis_do_csv(jmeno_souboru:str, hlavicka_csv:list[str], data:list[dict]):
    """
    funkce zapíše do souboru csv extrahovaná data,
    použit nedefaultní oddělovač "="
    """
    r = open(jmeno_souboru, mode="w",encoding="utf-8", newline="")
    z = csv.DictWriter(r, hlavicka_csv, restval="0", delimiter="=")
    z.writeheader()
    for a in data:
        del a["odkaz"]
        z.writerow(a)
    r.close()


def hlavni():
    odkazy, odkaz_zahranici = nacteni_vsech_odkazu()

    if overeni_vstupu(odkazy) == True:
        print("Získávám data.")
        obce_strany = []
        if  odkaz_zahranici == sys.argv[1]:
            for i in nacteni_vsech_zahranicnich_obci(sys.argv[1]):
                obce_strany.append(nacteni_stran(nacteni_souhrnu(i))) 

        else:
            for i in nacteni_vsech_obci(sys.argv[1]):
                obce_strany.append(nacteni_stran(nacteni_souhrnu(i)))

        zapis_do_csv(sys.argv[2], vytvoreni_hlavicky_csv(obce_strany), obce_strany)

if __name__ == "__main__":
    hlavni()
        
