import requests
from  bs4 import BeautifulSoup

url = "https://www.ceneo.pl/152762774"
page = requests.get(url)
parsed_html = BeautifulSoup(page.content, "html.parser")

container = parsed_html.find('div', class_="product-offer-summary")
price = container.find('span', class_="value")
price = price.text.strip().replace(" ", "").replace("\n", "")
print(price)