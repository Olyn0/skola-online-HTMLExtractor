import requests
from bs4 import BeautifulSoup
import sys
import os

loaddata = "postData/"+input("napiš název souboru na data např. postdata.txt....")
#loaddata=("postData/postdataZpravy.txt")
# Funkce pro načtení dat ze souboru
def load_post_data(file_path):
    post_data = {}
    url = None
    #test
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):  # Ignorujeme prázdné řádky a komentáře
                key, value = line.split("=", 1)
                if key == "URL":
                    url = value.strip()
                else:
                    post_data[key.strip()] = value.strip()
    return url, post_data

# Funkce pro získání hidden input hodnot
def get_hidden_value(soup, name):
    tag = soup.find("input", {"name": name})
    return tag["value"] if tag else ""

# Načtení přihlašovacích údajů
creds="credentials.txt"
if not os.path.exists("/Users/ondrej/credentials.txt"):
    creds = "credentials.txt"
else:
    creds = "/Users/ondrej/credentials.txt"


with open(creds, "r", encoding="utf-8") as file:
    user = file.readline().strip()
    password = file.readline().strip()

# Načtení URL a POST dat
target_url, post_data = load_post_data(loaddata)

if not target_url:
    print("❌ Chybí URL v souboru postdata.txt!")
    exit()

# Vytvoření session pro udržení cookies
session = requests.Session()
login_url = "https://aplikace.skolaonline.cz/SOL/Prihlaseni.aspx"

# Stáhneme login stránku, abychom získali hidden inputy
response = session.get(login_url)
soup = BeautifulSoup(response.text, "html.parser")

# Získání hidden input hodnot pro přihlášení
viewstate = get_hidden_value(soup, "__VIEWSTATE")
viewstategenerator = get_hidden_value(soup, "__VIEWSTATEGENERATOR")
eventvalidation = get_hidden_value(soup, "__EVENTVALIDATION")

# Přihlašovací údaje
login_data = {
        "__EVENTTARGET": "dnn$ctr994$SOLLogin$btnODeslat",
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": viewstategenerator,
        "__PREVIOUSPAGE": "",
        "__EVENTVALIDATION": eventvalidation,
        "JmenoUzivatele": user,
        "HesloUzivatele": password,
    }
# Hlavičky
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": login_url
}

# Odeslání přihlašovacího formuláře
response = session.post(login_url, data=login_data, headers=headers)

# Ověření přihlášení
if "Session Expired" in response.text or "Přihlášení" in response.text:
    print("❌ Přihlášení selhalo!")
    exit()
else:
    print("✅ Přihlášení úspěšné!")

# Načtení cílové stránky
response = session.get(target_url, headers=headers, cookies=session.cookies)
soup = BeautifulSoup(response.text, "html.parser")

# Aktualizace hidden input hodnot pro POST request
post_data["__VIEWSTATE"] = get_hidden_value(soup, "__VIEWSTATE")
post_data["__VIEWSTATEGENERATOR"] = get_hidden_value(soup, "__VIEWSTATEGENERATOR")
post_data["__EVENTVALIDATION"] = get_hidden_value(soup, "__EVENTVALIDATION")
post_data["__VIEWSTATE_SESSION_KEY"] = get_hidden_value(soup, "__VIEWSTATE_SESSION_KEY")

# Odeslání POST requestu
response = session.post(target_url, data=post_data, headers=headers, cookies=session.cookies)

# Uložení HTML odpovědi
file_path = "output.html"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"📄 Stránka uložena do {file_path}")