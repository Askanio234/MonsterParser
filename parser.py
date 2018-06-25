import json
import requests
from bs4 import BeautifulSoup


TARGET_URL = 'https://www.monster.com/jobs/q-financial-analyst-jobs.aspx?page=1'

MAIN_DATA_KEY = 'mainEntityOfPage'

MAX_PAGE = 2

DESCRIPTION_ID = 'JobDescription'


def get_html_page(url):
    request = requests.get(url)
    return request.text


def get_vacancies_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script', type='application/ld+json')
    for script in scripts:
        jsonifed_data = json.loads(script.get_text())
        if MAIN_DATA_KEY in jsonifed_data.keys():
            return jsonifed_data


def get_vacancies_urls(json_data):
    return [position['url'] for position in json_data['itemListElement']]


def get_vacancy_description(url):
    html = get_html_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    description = soup.find('div', id=DESCRIPTION_ID)
    return description.get_text()


if __name__ == '__main__':
    html = get_html_page(TARGET_URL)
    vacancies_data = get_vacancies_data(html)
    vacancies_urls = get_vacancies_urls(vacancies_data)
    desc = get_vacancy_description(vacancies_urls[0])
