# from multiprocessing import Pool
# import xlsxwriter
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response.text            #возвращает HTML код страницы


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find_all('a', class_='ared')

    links = []
    for td in tds:
        td = str(td)
        num_symbol_start = td.find('/')
        num_symbol_end = td.find('onclick') - 2
        link = 'http://www.hipavto.com.ua' + td[num_symbol_start:num_symbol_end] #+ '?simple=view'
        if link not in links:
            links.append(link)
    return links                  #получаем список всех ссылок на страницы товаров с описанием и марками авто




# def text_before_word(text, word):
#     line = text.split(word)[0].strip().strip('(').strip(')').replace('.',',')
#     return line


def get_page_data(html):
    # html = html + '#catalog-originals'
    soup = BeautifulSoup(html, 'lxml')
    # auto_models = soup.find('table', class_='get-info').find_all('tr')    #описание товаров
    auto_models = soup.find('div', id='catalog-originals').find_all('tr')

    cars = []
    # models_cars = []
    for value in auto_models:
        value = str(value)

        num_symbol_end = value.find('</td>')
        car_brand = value[9:num_symbol_end]     #определили название марки авто
        # cars.append(car_brand)

        num_symbol_start = value.find('</td> <td>') + 10
        car_models = value[num_symbol_start:].strip('</td> </tr>').replace('\xa0', ' ')
        car_models = str(car_models)

        cars.append(car_brand + ' - ' + car_models)

    #auto_models = soup.find('div', id='catalog - autos').find_all('tr')
    print(cars)


    # try:
    #     name = soup.find('span', class_='text-bold h3 text-gray text-large').text
    # except:
    #     name = ''
    # try:
    #     price = soup.find('span', id='quote_price').text
    # except:
    #     price = ''
    # try:
    #     delta = soup.find('span', class_='h2 text-semi-bold negative_change').text
    # except:
    #     delta = ''
    # data = {'name': name,
    #         'price': price,
    #         'delta': delta}
    # return data


# def write_csv(data):
#     try:
#         with open('coinmarketcap.csv', 'a') as f:
#             writer = csv.writer(f)
#             writer.writerow((data['name'],
#                              data['price'],
#                              data['delta']))
#             print(data['name'], 'parsed')
#     except:
#         exit('файл coinmarketcap.csv открыт')


def main():
    url = 'http://www.hipavto.com.ua/search/number/?article=OC+196&brand=34'
    all_links = get_all_links(get_html(url))

    # with Pool(2) as p:
    #     p.map(make_all, all_links)

    for index, url in enumerate(all_links):
        html = get_html(url)
        data = get_page_data(html)
        # try:
        #     workbook = xlsxwriter.Workbook('coinmarketcap.xlsx')
        #     worksheet = workbook.add_worksheet('data')
        #     worksheet.write(index, 0, (data['name'],
        #                                data['price'],
        #                                data['delta']))
        #     # worksheet.write(index, 1, data[index + 1])
        #     # worksheet.write(index, 2, data[index + 2])
        #
        #     workbook.close()
        # except:
        #     exit('файл coinmarketcap.xlsx открыт')
        # write_csv(data)


if __name__ == '__main__':
    main()
