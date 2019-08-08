import requests

from pages.all_orb_page import OrbPage
from URL_builder.poe_trade_url import PoeTradeUrl
from pages.transaction_page import TransactionPage


page_content = requests.get('http://currency.poe.trade').content
page = OrbPage(page_content)

orb_dict = {}
for orb in page.orbs:
    orb_dict[orb.name] = orb.id


reverse_orb_dict = dict(zip(orb_dict.values(), orb_dict.keys()))

# x = orb_dict.get('Chaos Orb')
#
# y = reverse_orb_dict.get('4')
# print(x)
# print(y)
#
#
# url_test = PoeTradeUrl('Legion', orb_dict.get('Chaos Orb'), orb_dict.get('Orb of Alteration'))
#
#
# print(type(url_test))
# print(url_test.url)

url_test = PoeTradeUrl('Legion', orb_dict.get('Chaos Orb'), orb_dict.get('Orb of Alteration'))

print(url_test)

page_content_two = requests.get(url_test.url).content

page_two = TransactionPage(page_content_two)

for orb in page_two.transactions:
    print(orb)



