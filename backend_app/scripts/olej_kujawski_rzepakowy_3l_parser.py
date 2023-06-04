import requests
from  bs4 import BeautifulSoup

url = "https://hurtownia-spozywcza.pl/kru-olej-kujawski-3l.html"
page = requests.get(url)
parsed_html = BeautifulSoup(page.content, "html.parser")

price = parsed_html.find('span', id="st_product_options-price-brutto")
price = price.text.strip().replace(" ", "").replace("\n", "").replace(",", ".")
print(price[:-2])