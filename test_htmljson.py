from bs4 import BeautifulSoup
import json
import xml.etree.ElementTree as ET


def extract_data(html_file, output_file, output_format='json'):
	with open(html_file, 'r', encoding='utf-8') as f:
		soup = BeautifulSoup(f, 'html.parser')

	data = {'tables': [], 'lists': []}

	# Extrakce tabulek
	for table in soup.find_all('table'):
		rows = []
		for tr in table.find_all('tr'):
			cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
			rows.append(cells)
		data['tables'].append(rows)

	# Extrakce seznamů
	for ul in soup.find_all('ul'):
		items = [li.get_text(strip=True) for li in ul.find_all('li')]
		data['lists'].append(items)

	for ol in soup.find_all('ol'):
		items = [li.get_text(strip=True) for li in ol.find_all('li')]
		data['lists'].append(items)

	# Uložení do souboru
	if output_format == 'json':
		with open(output_file, 'w', encoding='utf-8') as f:
			json.dump(data, f, ensure_ascii=False, indent=4)
	elif output_format == 'xml':
		root = ET.Element('data')

		for table in data['tables']:
			table_elem = ET.SubElement(root, 'table')
			for row in table:
				row_elem = ET.SubElement(table_elem, 'row')
				for cell in row:
					cell_elem = ET.SubElement(row_elem, 'cell')
					cell_elem.text = cell

		for lst in data['lists']:
			list_elem = ET.SubElement(root, 'list')
			for item in lst:
				item_elem = ET.SubElement(list_elem, 'item')
				item_elem.text = item

		tree = ET.ElementTree(root)
		tree.write(output_file, encoding='utf-8', xml_declaration=True)
	else:
		print("Neznámý formát výstupu")


# Použití
extract_data('output.html', 'extractZpravy/vystup.json', 'json')  # Nebo 'xml'
