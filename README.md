# SkolaOnline HTMLExtractor

## Popis
Tento projekt slouží k automatickému přihlašování do systému SkolaOnline a získávání dat pomocí HTTP požadavků. Skript se přihlásí pomocí uživatelských údajů, stáhne potřebné hidden input hodnoty, provede autentizaci a následně odešle požadované POST requesty pro získání dat.


## TODO
- Převést html obsah do zformátované podoby
  
## Požadavky
- Python 3.x (nejlépe 3.13)
- Knihovny uvedené v `requirements.txt`

## Instalace
1. Naklonujte repozitář:
   ```bash
   git clone <URL_REPOZITÁŘE>
   cd <NÁZEV_SLOŽKY>
   ```
2. Nainstalujte požadované knihovny:
   ```bash
   pip3 install -r requirements.txt
   ```

## Použití
1. Vytvořte soubor `credentials.txt` a zadejte přihlašovací údaje ve formátu:
   ```
   username
   password
   ```
2. Vytvořte soubor `postdata.txt` a definujte v něm požadované parametry POST requestu. Příklad souboru pro zobrazení kalendáře týdne, kde se nachází 12. únor, je následující:
   ```
   URL=https://aplikace.skolaonline.cz/SOL/App/Kalendar/KZK001_KalendarTyden.aspx
   __EVENTTARGET=calendarPart$kalendar
   calendarPart_kalendar=%3Cx%20PostData%3D%222025x3x2025x2x12x1%22%3E%3C/x%3E #2025x2x12 týden kde se nachází den 12. února
   calendarPart$kalendar$RBSelectionMode=Week
   CBZobrazitRozvrh=on
   CBZobrazitHodnoceni=on
   ```
   - `URL` definuje cílovou adresu požadavku.
   - Další řádky obsahují parametry ve formátu `klíč=hodnota`.
   - Řádky začínající `#` jsou ignorovány jako komentáře.
   - Některé POST parametry jsou získávány dynamicky ze stránky před odesláním požadavku, například:
     ```python
     post_data["__VIEWSTATE"] = get_hidden_value(soup, "__VIEWSTATE")
     post_data["__VIEWSTATEGENERATOR"] = get_hidden_value(soup, "__VIEWSTATEGENERATOR")
     post_data["__EVENTVALIDATION"] = get_hidden_value(soup, "__EVENTVALIDATION")
     post_data["__VIEWSTATE_SESSION_KEY"] = get_hidden_value(soup, "__VIEWSTATE_SESSION_KEY")
     ```
     Tyto hodnoty se mění při každém načtení stránky, proto je nelze předem definovat v souboru `postdata.txt`.

3. Spusťte skript:
   ```bash
   python gethtmlfrompostadata.py
   ```
4. Zadejte název souboru s POST daty, například:
   ```
   např. postdata.txt
   ```
5. Po úspěšném přihlášení a zpracování požadavku se HTML odpověď uloží do `output.html`.

## Možnosti využití
1. **Získávání známek**
   - Pomocí skriptu lze automaticky stáhnout a analyzovat známky ze systému SkolaOnline.

2. **Stahování školního kalendáře**
   - Skript umožňuje načíst kalendář událostí a rozvrh hodin.

3. **Získání zpráv**
   - Lze stáhnout přijaté zprávy a analyzovat jejich obsah.

4. **Možné rozšíření pro jiné stránky**
   - Skript lze upravit pro jakoukoliv stránku s přihlašováním a POST requesty, například:
   ```
   URL=https://mojestranka.cz/prihlaseni
   username=moje_jmeno
   password=moje_heslo
   ```
   - Stačí upravit parametry v `postdata.txt` podle struktury dané stránky.

## Struktura projektu
```
├── gethtmlfrompostadata.py  # Hlavní skript
├── credentials.txt          # Přihlašovací údaje
├── postdata.txt             # Soubor s POST daty
├── requirements.txt         # Seznam požadovaných knihoven
├── output.html              # Výstupní HTML soubor
```

## Poznámky
- Skript umožňuje přidávat další varianty POST dat podle potřeby.
- Při neúspěšném přihlášení skript zobrazí chybovou zprávu.

## Autor
Ondřej Šindelka
