import json
import time
import random
from string import ascii_uppercase
import requests
from bs4 import BeautifulSoup
from proxies import PROXIES_LIST


LETTERS = ascii_uppercase

TARGET_URL = 'https://www.monster.com/jobs/q-financial-analyst-jobs.aspx?page=1'

MAIN_DATA_KEY = 'mainEntityOfPage'

MAX_PAGE = 2

DESCRIPTION_ID = 'JobDescription'

MIN_SEC = 15
MAX_SEC = 20

HEADERS = {
    'User-Agent': 'Mozilla/5.0'
    '(Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}


#PROXIES = {
    #'https': 'https://80.211.169.186:8080'
#}

def print_proxy(proxy):
    print('Using - {}'.format(proxy))


def get_proxy(proxies_list):
    proxy = {}
    proxy[TARGET_URL.split(':')[0]] = random.choice(proxies_list)
    print_proxy(proxy)
    return proxy


def get_raw_html(request):
    if request.status_code == requests.codes.ok:
        return request.text
    else:
        print('STATUS CODE IS NOT 200')


def fetch_page(url, headers, proxies_list):
    proxies = get_proxy(proxies_list)
    try:
        request = requests.get(url, headers=headers, proxies=proxies)
        return get_raw_html(request)
    except requests.RequestException:
        print('Could not get response from the site')


def intialise_soup(html):
    return BeautifulSoup(html, 'html.parser')


def get_vacancies_data(html):
    soup = intialise_soup(html)
    scripts = soup.find_all('script', type='application/ld+json')
    for script in scripts:
        jsonifed_data = json.loads(script.get_text())
        if MAIN_DATA_KEY in jsonifed_data.keys():
            return jsonifed_data


def get_vacancies_urls(json_data):
    return [position['url'] for position in json_data['itemListElement']]


def format_description(description):
    return '{}\n'.format(description[1:])


def get_vacancy_description(url):
    time.sleep(random.randrange(MIN_SEC, MAX_SEC))
    html = fetch_page(url, HEADERS, PROXIES_LIST)
    if html is not None:
        soup = intialise_soup(html)
        description = soup.find('div', id=DESCRIPTION_ID)
        return format_description(description.get_text())
    else:
        return 'n/a\n'


def parse_vacancies_descriptions_from_page(vacancies_urls):
    return [get_vacancy_description(url) for url in vacancies_urls]


def write_to_file(descriptions, filename='output.txt'):
    with open(filename, 'w') as fh:
        fh.writelines(descriptions)


def parse_vacanies_page(TARGET_URL, page_num):
    pass

if __name__ == '__main__':
    html = fetch_page(TARGET_URL, HEADERS, PROXIES_LIST)
    vacancies_data = get_vacancies_data(html)
    vacancies_urls = get_vacancies_urls(vacancies_data)
    desc = parse_vacancies_descriptions_from_page(vacancies_urls[:2])
    write_to_file(desc)
