
import pandas as pd
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

price_list = []
product_list = []
local_list = []
link_list = []

# Iniciando Instancia Chrome
service = Service()
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(service=service, options=options)

# Acessar Site
# link = https://www.olx.com.br/imoveis/comercio-e-industria/aluguel/estado-sc
sleep(2)
# input('Cole o link da lista da OLX: ')
url = input('Cole o link da lista da OLX: ')
max_pages = int(input(
    'Digite a Quantidade de páginas que deseja coletar os dados [Digite "0" para todas as disponíveis]: '))
read_pages = 0
print('Abrindo Página...')
driver.get(url=url)


def goto_next_page():
    next_bt = driver.find_elements(By.CLASS_NAME, 'olx-core-button--link')
    print(next_bt)
    next_page_link = None

    for i in range(len(next_bt)):
        print(next_bt[i])
        try:
            next_page_link = next_bt[i].find_element(By.TAG_NAME, 'a')
            print(next_page_link)
            a_text = next_page_link.text
            print(a_text)
            if a_text == 'Próxima página':
                next_bt = next_bt[i]
                break
        except:
            continue

    _class = next_bt.get_attribute('class')

    if _class == 'olx-core-button olx-core-button--link olx-core-button--small':
        _url = next_page_link.get_attribute('href')
        driver.get(url=_url)
        get_data()

    elif _class == 'olx-core-button olx-core-button--link olx-core-button--small olx-core-button--disabled':
        print('ALL PAGES GET')
        make_dataframe()


def get_data():
    global driver
    global price_list
    global product_list
    global local_list
    global link_list
    global read_pages
    global max_pages
    # Encontrar dados por elementos na página
    e_list = driver.find_elements(By.CLASS_NAME, 'olx-ad-card--horizontal')
    print('\nReading product cards...')
    for item in e_list:
        content = item.find_element(
            By.CLASS_NAME, 'olx-ad-card__content--horizontal')
        # print(content)
        title = content.find_element(
            By.CLASS_NAME, 'olx-ad-card__title-link').find_element(By.TAG_NAME, 'h2').text
        # print(title)
        try:
            price = content.find_element(By.CLASS_NAME, 'olx-ad-card__details-price--horizontal').find_element(
                By.CLASS_NAME, 'olx-text--body-large').text.replace(' ', '')+',00'
        except:
            price = '----'
        # print(price)
        location = content.find_element(
            By.CLASS_NAME, 'olx-ad-card__location-date-container').find_element(By.TAG_NAME, 'p').text
        # print(location)
        link = content.find_element(
            By.CLASS_NAME, 'olx-ad-card__title-link').get_attribute('href')
        # print(link)

        product_list.append(title)
        price_list.append(price)
        local_list.append(location)
        link_list.append(link)
    print('\nREAD ALL PAGE CARDS')
    if max_pages != 0:
        read_pages += 1
        if read_pages == max_pages:
            print('ALL PAGES GET')
            make_dataframe()
        else:
            goto_next_page()
    else:
        goto_next_page()


def make_dataframe():
    print('Fazendo DATAFRAME')
    global product_list
    global price_list
    print(f'products = {len(product_list)} | prices = {
          len(price_list)} | locations = {len(local_list)} | links = {len(link_list)}')
    data = {'PRODUTO': product_list, 'PREÇO': price_list,
            'LOCALIDADE': local_list, 'PÁGINA NA LOJA': link_list}
    dataframe = pd.DataFrame(data)
    print(dataframe.to_string())
    #dataframe.to_csv(r'./output/product_data_olx.csv', sep='\t',
                     #encoding='utf-8', header='true')
    dataframe.to_csv(r'C:\Users\aline.carvalho\PycharmProjects\uso_selenium\output\product_data_olx.csv', sep='\t',
                     index=False)


print('Iniciando Coleta de Dados...')
get_data()
