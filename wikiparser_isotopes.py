from wikiparser import *
from htmlparser import parse_from_file
import os
import json


def download_content():
    with open('files/isotopes/wikilinks.txt') as file:
        for line in (line.strip() for line in file):
            url = 'https://en.wikipedia.org' + line
            page = requests.get(url)
            html_string = page.content.decode('utf-8')
            with open('files/isotopes' + line[5:] + '.html', 'w') as html_file:
                html_file.write(html_string)
            print(url + ' downloaded')


def html_to_json():
    non_parsable = ''
    for filename in ('files/isotopes/html_files/' + fn for fn in os.listdir('files/isotopes/html_files')):
        page = parse_from_file(filename)
        raw_tables = page.get_elements('table')
        tables = list()
        for table in raw_tables:
            table.remove(attribute=('style', 'display:none;'))
            table.remove(attribute=('style', 'display:none'))
            table_data = list()
            for row in table:
                try:
                    if row[0].name in ['td', 'th']:
                        values = parse_row(row)
                        table_data.append(values)
                except AttributeError:
                    pass
            tables.append(table_data)

        best_table = None
        for table in tables:
            first_row = table[0]
            if first_row[0] == 'nuclidesymbol':
                best_table = table
                break

        if best_table:
            name = filename.split('/')[-1].split('.')[0]
            with open('files/isotopes/json_files_2/' + name + '.json', 'w') as jsonfile:
                json.dump(best_table, jsonfile, separators=(',', ':'), indent=4)

            print(filename + ' parsed. ' + str(len(tables)) + ' tables found.')
        else:
            print(filename + ' parsed. No usable tables found.')
            non_parsable += filename
    with open('files/isotopes/non_parsable_html_files.txt', 'w') as file:
        file.write(non_parsable)


def process_json_data():
    isotopes_data = list()
    non_standard_isotopes = str()
    for filename in ('files/isotopes/json_files/' + fn for fn in os.listdir('files/isotopes/json_files')):
        with open(filename) as json_file:
            json_data = json_file.read()
        table = json.loads(json_data)

        head_row = table.pop(0)
        if len(head_row) != 10:
            non_standard_isotopes += filename + '\n'

        isotope_data = list()
        for row in (row for row in table if len(row) in [8, 10]):
            isotope = dict()
            isotope['z'] = row[1]
            isotope['n'] = row[2]
            isotope['sym'] = row[0]
            isotope['m'] = row[3]
            isotope['hl'] = row[4]
            isotope['spin'] = row[-3]
            isotope['mf'] = row[-2]
            isotope['mfr'] = row[-1]
            if len(row) == 8 and row[4] not in ['stable', 'Stable']:
                continue
            isotope_data.append(isotope)
        isotopes_data.append(isotope_data)
    with open('files/isotopes/non_standard_isotopes.txt', 'w') as file:
        file.write(non_standard_isotopes)
    with open('files/isotopes/data.json', 'w') as file:
        json.dump(isotopes_data, file, separators=(',', ':'), indent=4)


def temp():
    with open('files/isotopes/non_standard_isotopes.txt') as file:
        for json_filename_in in (fn.strip() for fn in file):
            with open(json_filename_in) as json_file_in:
                file_data = json_file_in.read()
                json_filename_out = 'files/isotopes/json_files_non_standard/' + json_filename_in.split('/')[-1]
                with open(json_filename_out, 'w') as json_file_out:
                    json_file_out.write(file_data)


temp()
