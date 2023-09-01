import requests
import bs4
import json
import fake_headers


headers_gen = fake_headers.Headers(browser='firefox', os='win')

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
response = requests.get(url, headers=headers_gen.generate())
main_html = response.text
main_soup = bs4.BeautifulSoup(main_html, 'lxml')
vacancies = main_soup.find_all(class_='vacancy-serp-item-body__main-info')

result_list = []
for vacancy in vacancies:
    link = vacancy.find('a', class_='serp-item__title')['href']
    company = vacancy.find('div', class_='vacancy-serp-item__meta-info-company').text.strip()
    city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text.strip()
    salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    if salary:
        salary = salary.text.strip()
    else:
        salary = 'Не указана'
    response_link = requests.get(link, headers=headers_gen.generate())
    response_text = response_link.text
    links_parsed = bs4.BeautifulSoup(response_text, 'lxml')
    description = links_parsed.find('div', class_='g-user-content')
    if 'django' or 'flask' in description.lower():
        vacancy_info = {
            'link': link,
            'company': company,
            'city': city,
            'salary': salary
        }
        result_list.append(vacancy_info)


with open('dz_scraping.json', 'w', encoding='utf-8') as file:
    json.dump(result_list, file, ensure_ascii=False, indent=2)








