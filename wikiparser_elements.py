import os
import json
import requests

from htmlparser import parse_from_url, parse_from_file


def find_the_urls():
    url = 'https://en.wikipedia.org/wiki/Periodic_table'
    page = parse_from_url(url)
    for link in page.get_links():
        print(link)


def download_content():
    with open('files/elements/wikilinks.txt') as file:
        for line in (line.strip() for line in file):
            url = 'https://en.wikipedia.org' + line
            page = requests.get(url)
            html_string = page.content.decode('utf-8')
            with open('files/elements' + line[5:] + '.html', 'w') as html_file:
                html_file.write(html_string)
            print(url + ' downloaded')


def html_to_json():
    data_to_collect = [('Atomic number (Z)', 'Z', True),
                       ('Name, symbol', 'symbol', True),
                       ('Appearance', 'appearance', False),
                       ('Group, block', 'Group, block', True),
                       ('Period', 'period', True),
                       ('Element category', 'category', False),
                       ('Standard atomic weight', 'atomic weight', True),
                       ('Electron configuration', 'configuration', True),
                       ('per shell', 'per shell', True),
                       ('Color', 'color', False),
                       ('Phase', 'phase', False),
                       ('Melting point', 'melting point', True),
                       ('Boiling point', 'boiling point', True),
                       ('Density', 'density', True),
                       ('when liquid, at m.p.', 'density liquid at mp', False),
                       ('when liquid, at b.p.', 'density liquid at bp', False),
                       ('Triple point', 'triple point', True),
                       ('Critical point', 'critical point', True),
                       ('Heat of fusion', 'heat of fusion', True),
                       ('Heat of vaporization', 'heat of vaporizatio', True),
                       ('Molar heat capacity', 'molar heat capacity', True),
                       ('Oxidation states', 'oxidation states', True),
                       ('ElectronegativityPauling scale:', 'electronegativity', True),
                       ('Covalent radius', 'covalent radius', True),
                       ('Van der Waals radius', 'van der waals radius', True),
                       ('Crystal structure', 'crystal structure', True),
                       ('Speed of sound', 'speed of sound', False),
                       ('Thermal conductivity', 'thermal conductivity', False),
                       ('CAS Number', 'cas number', False),
                       ('Magnetic ordering', 'magnetic ordering', False)]
    for filename in ('files/elements/html_files/' + fn for fn in os.listdir('files/elements/html_files')):
        page = parse_from_file(filename)
        table = page.get_elements('table')[0]
        table.remove(attribute=('style', 'display:none;'))
        table.remove(attribute=('style', 'display:none'))
        raw_data = dict()
        for row in table:
            row_text = row.to_text()
            for item in data_to_collect:
                if row_text[0:len(item[0])] == item[0]:
                    raw_data[item[1]] = row_text[len(item[0]):]
        name = filename.split('/')[-1].split('.')[0]
        with open('files/elements/json_files/' + name + '.json', 'w') as jsonfile:
            json.dump(raw_data, jsonfile, separators=(',', ':'), indent=4)


def remove_brackets(string, max_number=10):
    for _ in range(max_number):
        left_bracket = string.find('[')
        right_bracket = string.find(']')
        if left_bracket == -1 or right_bracket == -1:
            return string
        if left_bracket > right_bracket:
            raise ValueError
        string = string[0:left_bracket] + string[right_bracket+1:]
    return string


def remove_round_brackets(string, max_number=10):
    for _ in range(max_number):
        left_bracket = string.find('(')
        right_bracket = string.find(')')
        if left_bracket == -1 or right_bracket == -1:
            return string
        if left_bracket > right_bracket:
            raise ValueError
        string = string[0:left_bracket] + string[right_bracket+1:]
    return string


def replace_signs(string):
    string = string.replace('\u00b7', '*')
    string = string.replace('\u200b', '')
    string = string.replace('\u2212', '-')
    string = string.replace('\u2013', '-')
    string = string.replace('\u00b0', '°')
    string = string.replace('\u00b1', '±')
    return string


def edit_string(string):
    string = remove_brackets(string)
    string = remove_round_brackets(string)
    string = replace_signs(string)
    string = string.strip()
    return string


def only_numerics(string):
    new_string = ''
    for item in string:
        if item in '0123456789.-,':
            new_string += item
    return new_string


def edit_json():
    with open('files/elements.json', 'r') as jsonfile:
        elements_data = json.load(jsonfile)

    for filename in ('files/elements/json_files/' + fn for fn in os.listdir('files/elements/json_files')):
        with open(filename) as file:
            element = json.load(file)
        number = int(element['Z'])
        element_dict = elements_data[number]

        attr_name = 'configuration'
        try:
            string = element['configuration']
            element_dict[attr_name] = string.strip()
            print(element_dict[attr_name])
        except (KeyError, ValueError):
            element_dict[attr_name] = None
            print(filename)

        elements_data[number] = element_dict

    with open('files/elements.json', 'w') as jsonfile:
        json.dump(elements_data, jsonfile, separators=(',', ':'), indent=4)


edit_json()

# to remove: color, heat of evaporation
