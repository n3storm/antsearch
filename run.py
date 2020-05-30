"""ant search"""
import requests
from bs4 import BeautifulSoup

stores = [
    ('https://www.antderground.com/categoria-producto/hormigas/','wp',),
    ('https://antkit.es/collections/queen-ants','wp',),
    ('https://anthouse.es/es/38-hormigas-gratis','ps',),
    ('https://hormigueando.com/22-hormigas','ps',),
    ('https://anthillshop.es/13-hormigas','ps',),
    ('https://labellaant.com/comprar/hormigas/','wp',),
    ]


class ShopItem():
    def __init__(self, text):
        self.html = BeautifulSoup(text, 'html.parser')
        self.get_items()
    
class WoocommerceItem(ShopItem):
    def get_items(self):
        self.items = self.html.body.find_all('li',class_="product")
    
    def build(self, item):
        _dict = {}
        if 'instock' in item.get('class'):
            _dict['title'] = item.find('a', class_="title").text
            _dict['link'] = item.find('a', class_="title").get('href')
            _dict['shop'] = _dict['link'].split('/')[2]
        else: return None
        return _dict
                    
class PrestashopItem(ShopItem):
    def get_items(self):
        self.items = self.html.body.main.section.find_all('article')
        
    def build(self, item):
        _dict = {}
        if 'product-unavailable' not in item.find('div', class_="product-availability").span.get('class'):
            _dict['title'] = item.find('h3', class_="product-title").a.text
            _dict['link'] = item.find('h3', class_="product-title").a.get('href')
            _dict['shop'] = _dict['link'].split('/')[2]
        else: return None
        return _dict
        

full_items = []
for store in stores:
    url, software = store
    r = requests.get(url)
    if software == 'ps':
        shop = PrestashopItem(r.text)
    elif software == 'wp':
        shop = WoocommerceItem(r.text)
    for item in shop.items:
        full_item = shop.build(item)
        if full_item:
            full_items.append(full_item)

print("**Hormigas Publicitadas Actualmente**")
print("-" * 25)
for entry in full_items:
    print('**{}** ({})\n__{}__'.format(entry['title'],entry['shop'],entry['link']))
