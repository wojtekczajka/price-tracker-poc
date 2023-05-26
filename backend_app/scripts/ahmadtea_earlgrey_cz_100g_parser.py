import requests
from  bs4 import BeautifulSoup

url = "https://hurtownia-spozywcza.pl/earl-grey-20tb-alu-ahmad-tea.html"
page = requests.get(url)
parsed_html = BeautifulSoup(page.content, "html.parser")

price = parsed_html.find('span', id="st_product_options-catalogue-brutto")
price = price.text.strip().replace(" ", "").replace("\n", "").replace(",", ".").replace("z", "").replace("ł", "")
print(price)