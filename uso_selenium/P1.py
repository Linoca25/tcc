from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time


chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
service = Service("./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://www.imovelweb.com.br/apartamentos-aluguel-rio-de-janeiro-rj.html')
time.sleep(3)