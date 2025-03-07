# Projekt: SkolaOnline Scraper

## Popis
Tento projekt slouží k automatickému přihlašování do systému SkolaOnline a získávání dat pomocí HTTP požadavků. Skript se přihlásí pomocí uživatelských údajů, stáhne potřebné hidden input hodnoty, provede autentizaci a následně odešle požadované POST requesty pro získání dat.

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
   pip install -r requirements.txt
   ```

## Použití
1. Vytvořte soubor `credentials.txt` a zadejte přihlašovací údaje ve formátu:
   ```
   username
   password
   ```
2. Vytvořte soubor `postdata.txt` a definujte v něm požadované parametry POST requestu. Příklad souboru pro zoobrazení kalendáře týdne, kde se náchází 12.únor je následující:
   ```)
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

3. Spusťte skript:
   ```bash
   python gethtmlfrompostadata.py
   ```
4. Zadejte název souboru s POST daty, například:
   ```
   napiš název souboru na data např. postdata.txt....
   ```
5. Po úspěšném přihlášení a zpracování požadavku se HTML odpověď uloží do `output.html`.

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

