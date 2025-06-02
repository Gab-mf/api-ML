import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By

url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02'

response = requests.get(url)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find('table', {'class':'tb base tb dados'})

rows = table.find_all('tr')

data = []

for row in rows:
    cells = row.find_all(['th', 'td'])
    cells_text = [cells.get_text(strip=True) for cell in cells]
    data.append(cells_text)

df = pd.DataFrame(data[1:], columns=data[0])

print(df.head())