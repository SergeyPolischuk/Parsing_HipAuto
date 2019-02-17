# from multiprocessing import Pool
# import xlsxwriter
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

#Это тестовый комментарий!

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
    return links               #получаем список всех ссылок на страницы товаров с описанием и марками авто


def get_page_data(html):
    #get_original_cars
    soup = BeautifulSoup(html, 'lxml')
    ## auto_models = soup.find('table', class_='get-info').find_all('tr')    #описание товаров

    try:
        brands = soup.find_all('a', class_='fancy_inline droppeda')
        articles = soup.find_all('a', class_='ared')
        # descriptions = soup.find_all('td', class_='g-descr cell ')
        # terms = soup.find_all('td', class_='g-delivery smallprice cell ')
        # remainders = soup.find_all('td', class_='g-box cell ')
        prices = soup.find_all('span', itemprop='price')
    except:
        brands = []
        articles = []
        prices = []


    # for brand in brands:
    #     brand = str(brand)
    #     num_first_symbol = brand.find('>') + 1
    #     num_last_symbol = brand.find('</a>')
    #     print(brand[num_first_symbol:num_last_symbol])

    # for article in articles:
    #     article = str(article).replace('●', '')
    #     num_first_symbol = article.find('<b>') + 3
    #     num_last_symbol = article.find('</b>')
    #     print(article[num_first_symbol:num_last_symbol])

    # for price in prices:
    #     price = str(price).replace('.', ',')
    #     num_first_symbol = price.find('>') + 1
    #     num_last_symbol = price.find('</span>')
    #     print(price[num_first_symbol:num_last_symbol])


    #_________________________________________

    # try:
    #     auto_models = soup.find('div', id='catalog-originals').find_all('tr')
    # except:
    #     auto_models = []
    #
    # original_cars = []
    #
    # for value in auto_models:
    #     value = str(value)
    #
    #     num_symbol_end = value.find('</td>')
    #     car_brand = value[9:num_symbol_end]     #определили название марки авто
    #
    #     num_symbol_start = value.find('</td> <td>') + 10
    #     car_models = value[num_symbol_start:].strip('</td> </tr>').replace('\xa0', ' ')
    #     car_models = str(car_models)            #определили модели марки авто
    #
    #     original_cars.append(car_brand + ' - ' + car_models)

    # _________________________________________

    # try:
    #     auto_models2 = soup.find('div', class_="bmrk").find_all('a')
    # except:
    #     auto_models2 = []
    #
    # links_applicability_cars = []
    # applicability_cars = []
    #
    # for value in auto_models2:
    #     value = str(value)
    #     num_symbol_start = value.find('this,')
    #     card_number = value[num_symbol_start + 7:num_symbol_start + 14]  # определили номер запчасти onclick="get_models
    #
    #     num_symbol_end = value.find(')')
    #     car = value[num_symbol_start + 17:num_symbol_end - 1]  # определили марку машины
    #
    #     html = str(get_html('http://www.hipavto.com.ua/detail/models/?artid=' + card_number + '&mark=' + car))[31:].split('<a')
    #
    #     x1 = html[1].find('this') + 17
    #     x2 = html[1].find(',', x1) - 1
    #
    #     if html[1][x1:x2].find('%') > 0:
    #         x = html[1][x1:x2].find('%')
    #         car = html[1][x1:x2][:x]
    #     else:
    #         car = html[1][x1:x2]
    #
    #     print(car)
    #
    #     for value in html:
    #         num_symbol_start = value.find('>') + 1
    #         num_symbol_end = value.find('</a>')
    #         if value[num_symbol_start:num_symbol_end] != "":
    #             print(value[num_symbol_start:num_symbol_end])


    # ________________________________________

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
    all_links2 = get_page_data(get_html(url))

    # with Pool(2) as p:
    #     p.map(make_all, all_links)

    for index, url in enumerate(all_links):
        html = get_html(url)
        # data = get_page_data(html)
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
