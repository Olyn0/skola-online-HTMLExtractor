from bs4 import BeautifulSoup
import json
import re


def parse_subject(subject):
	match = re.match(r'([A-Za-z]+)(\d+)\.(\w)(\d+)', subject)
	if match:
		predmet = match.group(1)
		trida = f"{match.group(2)}.{match.group(3)}"
		ucebna = f"uč. {match.group(4)}"
		return f"{predmet}, {trida}, {ucebna}"
	return subject  # Pokud nesedí na formát, necháme beze změny


def extract_schedule(html_file, output_file):
	with open(html_file, 'r', encoding='utf-8') as f:
		soup = BeautifulSoup(f, 'html.parser')

	schedule = []

	# Najdeme tabulku s rozvrhem
	table = soup.find('table', {'id': 'CCADynamicCalendarTable'})
	if not table:
		print("Tabulka s rozvrhem nebyla nalezena.")
		return

	rows = table.find_all('tr')[1:]  # Vynecháme hlavičku

	for row in rows:
		cols = row.find_all('td')
		if not cols:
			continue

		# První sloupec je den v týdnu + datum
		den_td = row.find('th')
		if not den_td:
			continue
		den_datum = den_td.get_text(strip=True)

		# Rozdělení dne a datumu (např. "Út11.2." → "Úterý", "11.2.")
		match = re.match(r'(Po|Út|St|Čt|Pá)(\d{1,2}\.\d{1,2}\.)?', den_datum)
		if match:
			den = {"Po": "Pondělí", "Út": "Úterý", "St": "Středa", "Čt": "Čtvrtek", "Pá": "Pátek"}.get(match.group(1),
			                                                                                           match.group(1))
			datum = match.group(2) if match.group(2) else ""
		else:
			den, datum = den_datum, ""

		# Zbytek sloupců jsou předměty (odstraníme pouze dny a datumy ze seznamu, ale ponecháme opakující se hodiny)
		predmety = [col.get_text(strip=True) for col in cols if
		            col.get_text(strip=True) and col.get_text(strip=True) != match.group(1) and col.get_text(
			            strip=True) != datum]

		# Odebrání každého druhého záznamu (ponecháme jen liché indexy)
		predmety = [predmety[i] for i in range(len(predmety)) if i % 2 == 0]

		# Upravíme formát předmětů
		predmety = [parse_subject(predmet) for predmet in predmety]

		schedule.append({
			'den': den,
			'datum': datum,
			'predmety': predmety
		})

	# Uložíme do JSON souboru
	with open(output_file, 'w', encoding='utf-8') as f:
		json.dump(schedule, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
	extract_schedule('/Users/ondrej/skolaonline/output.html', 'rozvrh.json')