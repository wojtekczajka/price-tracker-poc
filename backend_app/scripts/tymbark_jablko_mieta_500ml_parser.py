import requests
from  bs4 import BeautifulSoup

url = "https://hurtownia-spozywcza.pl/tymbark-napoj-aseptic-jab-mieta-aseptic500ml.html"
page = requests.get(url)
parsed_html = BeautifulSoup(page.content, "html.parser")

price = parsed_html.find('span', id="st_product_options-price-brutto")
price = price.text.strip().replace(" ", "").replace("\n", "").replace(",", ".")
print(price[:-2])