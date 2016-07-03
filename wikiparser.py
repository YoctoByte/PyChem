from htmlparser import parse_from_url, parse_from_file
import json
import requests


def parse_page_to_json(page, url):
    json_data = list()
    page_raw = requests.get(url)
    html_string = page_raw.content.decode('utf-8')
    with open('files/isotopes/' + url.split('/')[-1] + '.html', 'w') as file:
        file.write(html_string)
    tables = page.get_elements('table')
    for table in tables:
        table.remove(attribute=('style', 'display:none;'))
        table.remove(attribute=('style', 'display:none'))
        print(table)

        table_data = list()
        for row in table:
            if row[0].name in ['td', 'th']:
                values = parse_row(row)
                table_data.append(values)
        json_data.append(table_data)

    with open('files/isotopes/' + url.split('/')[-1] + '.json', 'w') as jsonfile:
        json.dump(json_data, jsonfile, separators=(',', ':'), indent=4)


def parse_row(row):
    values = list()
    for item in row:
        value = item.to_text()
        values.append(_parse_value(value))
    return values


def _parse_value(string):
    if string in ['–', '']:
        return None
    string = string.replace('\n', '')
    old_string = string

    # left, right = string.find('('), string.find(')')
    # if left != -1 and right != -1:
    #     if left == 0:
    #         string == string[1:-1]
    #     else:
    #         string = string[0:left-1]
    #         # todo: significance

    # if string[0] == '[' and string[-1] == ']':
    #     string = string[1:-1]
    #     # todo: estimate

    try:
        value = float(string)
        if value.is_integer():
            value = int(value)
    except ValueError:
        value = old_string

    return value

url = 'https://en.wikipedia.org/wiki/Isotopes_of_hydrogen'
page = parse_from_file('files/isotopes/Isotopes_of_hydrogen.html')
# page = parse_from_url(url)
parse_page_to_json(page, url)
