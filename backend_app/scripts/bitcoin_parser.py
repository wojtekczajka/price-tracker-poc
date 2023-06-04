import requests
from  bs4 import BeautifulSoup

url = "https://www.binance.com/en/price/bitcoin"
page = requests.get(url)
parsed_html = BeautifulSoup(page.content, "html.parser")

price = parsed_html.find('div', class_="css-12ujz79")
#price = price.find('span')
price = price.text.strip().replace(",", "")
print(price[2:])