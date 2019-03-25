# import xlsxwriter
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response.text            #возвращает HTML код страницы


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    try:
        brands = soup.find_all('a', class_='fancy_inline droppeda')
    except:
        brands = []

    try:
        articles = soup.find_all('a', class_='ared')
    except:
        articles = []

    try:
        descriptions = soup.find_all('td', class_='g-descr')
    except:
        descriptions = []

    try:
        remainders = soup.find_all('td', class_='g-box cell')
    except:
        remainders = []

    try:
        prices = soup.find_all('span', itemprop='price')
    except:
        prices = []

    brands_list = []
    for brand in brands:
        brand = str(brand)
        brand = brand.replace('Ë', 'E')
        num_first_symbol = brand.find('>') + 1
        num_last_symbol = brand.find('</a>')
        brands_list.append(brand[num_first_symbol:num_last_symbol])

    articles_list = []
    for article in articles:
        article = str(article).replace('●', '')
        num_first_symbol = article.find('<b>') + 3
        num_last_symbol = article.find('</b>')
        articles_list.append(article[num_first_symbol:num_last_symbol])

    descriptions_list = []
    for description in descriptions:
        description = str(description.find('a').contents).strip('[').strip("'")
        num_last_symbol = description.find('<') - 4
        descriptions_list.append(description[:num_last_symbol].strip(' ').rstrip(' '))

    # remainders_list = []
    # for remainder in remainders:
    #     remainder = str(remainder.contents)
    #     num_first_symbol = remainder.find('</span>') + 10
    #     num_last_symbol = remainder.find('</td>') - 1
    #     remainders_list.append(remainder[num_first_symbol:num_last_symbol].strip('  ').strip(' '))

    prices_list = []
    for price in prices:
        prices_list.append(str(price.contents).strip(']').strip('[').strip("'").replace('.', ','))


    data = []
    for num in range(len(brands_list)):
        try:
            brand = brands_list[num]
        except:
            brand = ''

        try:
            article = articles_list[num]
        except:
            article = ''

        try:
            description = descriptions_list[num]
        except:
            description = ''

        # try:
        #     remainder = remainders_list[num]
        # except:
        #     remainder = ''

        try:
            price = prices_list[num]
        except:
            price = ''

        product_row = {'brand': brand,
            'artcile': article,
            'description': description,
            # 'remainder': remainder,
            'price': price}
        data.append(product_row)
    return data

def write_csv(data):
    with open('hipauto.csv', 'a') as f:
        writer = csv.writer(f)
        for key in data:
            writer.writerow((
                key['brand'],
                key['artcile'],
                key['description'],
                # key['remainder'],
                key['price']))

def main():
    url = 'http://www.hipavto.com.ua/search/number/?article=OC+196&brand=34'
    all_data = get_page_data(get_html(url))
    write_csv(all_data)

    # for i, url in enumerate(all_data):
    #     html = get_html(url)
    #     data = get_page_data(html)
    #     write_csv(i, data) #закомментировать для получения бренд/артикул/описание/цена/количество

if __name__ == '__main__':
    main()