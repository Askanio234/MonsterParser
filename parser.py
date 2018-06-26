import argparse
import json
import time
import random
import requests
from bs4 import BeautifulSoup
from proxies import PROXIES_LIST


TARGET_URL = 'https://www.monster.com/jobs/q-financial-analyst-jobs.aspx'

MAIN_DATA_KEY = 'mainEntityOfPage'

MAX_RETRIES = 2

MAX_PAGE = 2

DESCRIPTION_ID = 'JobDescription'

MIN_SEC = 5
MAX_SEC = 15

HEADERS = {
    'User-Agent': 'Mozilla/5.0'
    '(Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}


def print_proxy(proxy):
    print('Using - {}'.format(list(proxy.values())[0]))


def get_proxy(proxies_list):
    proxy = {}
    proxy[TARGET_URL.split(':')[0]] = random.choice(proxies_list)
    print_proxy(proxy)
    return proxy


def get_raw_html(request):
    if request.status_code == requests.codes.ok:
        return request.text
    else:
        print('status code is not 200')


def fetch_page(url, headers, proxies_list):
    proxies = get_proxy(proxies_list)
    try:
        request = requests.get(url, headers=headers, proxies=proxies)
        return get_raw_html(request)
    except requests.RequestException:
        print('No response')
        pass


def fetch_page_with_retry(url, headers, proxies, max_num_retries):
    html = None
    retries = 0
    while retries < max_num_retries and html is None:
        time.sleep(random.randrange(MIN_SEC, MAX_SEC))
        html = fetch_page(url, HEADERS, PROXIES_LIST)
        retries += 1
    return html


def intialise_soup(html):
    return BeautifulSoup(html, 'html.parser')


def determine_max_pages(url):
    html = fetch_page_with_retry(url, HEADERS, PROXIES_LIST, 5)
    if html is not None:
        soup = intialise_soup(html)
        number = soup.find('input', id='totalPages')
        return int(number.get('value'))
    else:
        print('Failed to determine max_pages')


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
    return '{}\n'.format(description[1:].replace('\n', ' '))


def get_vacancy_description(url):
    print('Parsing - {}'.format(url))
    html = fetch_page_with_retry(url, HEADERS, PROXIES_LIST, MAX_RETRIES)
    if html is not None:
        soup = intialise_soup(html)
        description = soup.find('div', id=DESCRIPTION_ID)
        return format_description(description.get_text())
    return 'n/a\n'


def parse_vacancies_descriptions_from_page(vacancies_urls):
    return [get_vacancy_description(url) for url in vacancies_urls]


def write_to_file(descriptions, filename='output.txt'):
    with open(filename, 'a') as fh:
        fh.writelines(descriptions)


def parse_vacanies_page(target_url, page_num):
    url = '{}?page={}'.format(target_url, page_num)
    html = fetch_page_with_retry(url, HEADERS, PROXIES_LIST, MAX_RETRIES)
    if html is not None:
        vacancies_data = get_vacancies_data(html)
        vacancies_urls = get_vacancies_urls(vacancies_data)
        desc = parse_vacancies_descriptions_from_page(vacancies_urls)
        write_to_file(desc)
    else:
        print('Failed to parse pagenum {}'.format(page_num))


def parse_main(url, limit):
    page_num = 1
    max_pages = determine_max_pages(url)
    while page_num <= max_pages and page_num <= limit:
        parse_vacanies_page(url, page_num)
        page_num += 1


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Target_url",
                        default=TARGET_URL, required=False)
    parser.add_argument("--max_pages", help="Max pages to parse",
                        type=int, default=2, required=False)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    parse_main(args.url, args.max_pages)
