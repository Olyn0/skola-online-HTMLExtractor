from bs4 import BeautifulSoup
import json
import re


def clean_text(text):
	text = re.sub(r'\s+', ' ', text)  # Odstraní nadbytečné mezery
	text = re.sub(r'\xa0', ' ', text)  # Odstraní speciální mezery
	text = text.strip()  # Ořízne mezery na začátku a konci
	return text


def extract_messages(html_file, output_file):
	with open(html_file, 'r', encoding='utf-8') as f:
		soup = BeautifulSoup(f, 'html.parser')

	messages = []

	# Správná tabulka je s indexem 15
	tables = soup.find_all('table')
	if len(tables) <= 15:
		print("Tabulka se zprávami nebyla nalezena.")
		return

	rows = tables[15].find_all('tr')[1:]  # Vynecháme hlavičku

	for row in rows:
		cols = [col.get_text(strip=True) for col in row.find_all('td')]

		# Ověříme, že řádek má alespoň 4 sloupce a ignorujeme první prázdný sloupec
		if len(cols) >= 5 and cols[0] == "":
			cols = cols[1:]  # Posuneme se o jeden sloupec doprava

		if len(cols) >= 4:
			odesilatel, predmet, obsah, datum = cols[:4]
			obsah = clean_text(obsah)  # Vyčištění obsahu zprávy
		else:
			continue

		# Přidáme do seznamu zpráv
		messages.append({
			'odesilatel': odesilatel,
			'predmet': predmet,
			'datum': datum,
			'obsah': obsah
		})

	# Uložíme do JSON souboru
	with open(output_file, 'w', encoding='utf-8') as f:
		json.dump(messages, f, ensure_ascii=False, indent=4)

extract_messages('../output.html', 'output.json')