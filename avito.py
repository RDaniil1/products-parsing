from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from pprint import pprint
import shutil
import requests
from pathlib import Path

class Product:
    def __init__(self, info_link='', img_path='', price='', description='', name=''):
        self.info_link = info_link
        self.img_path = img_path
        self.price = price
        self.description = description
        self.name = name
    
    def __str__(self):
        if self.info_link:
            return f"""
                {self.info_link}
                {self.img_path}
                {self.price}
                {self.description}
                {self.name}"""
        else: return ''

def get_avito_products(product_name: str, town='all', _filter='', amount=5) -> list[Product]:
    base_url = 'https://avito.ru'
    product_name = product_name.replace(' ', '+')

    if _filter not in ['default', 'cheaper', 'expensive', 'date']:
        return [Product()]
    
    match _filter:
        case 'default':
            _filter = ''
        case 'cheaper':
            _filter = '1'
        case 'expensive':
            _filter = '2'
        case 'date':
            _filter = '104'
    
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    
    driver = Firefox(firefox_options)
    url = f'{base_url}/{town}?q={product_name}&s={_filter}'
    driver.get(url)

    # product item 
    # driver.find_element(By.CSS_SELECTOR, "div[class^='iva-item-root-']").click()

    # element_dispatcher = {
    #     'name' : "h3[class^='styles-module-root-TWVKW']",
    #     'price' : "span[class='']",
    #     'description' : "p[style^='-webkit-line-cla']",
    #     'info_link' : "a[class='iva-item-sliderLink-uLz1v']",
    #     'img_link' : "img[class^='photo-slider-image']"
    # }

    # for name, pattern in element_dispatcher:
    #     if name not in ['info_link', 'img_link']:
    #         driver.find_elements(By.CSS_SELECTOR, pattern)[:amount]
    
    # product name
    names = driver.find_elements(By.CSS_SELECTOR, "h3[class^='styles-module-root-TWVKW']")[:amount]

    # product price
    prices = driver.find_elements(By.CSS_SELECTOR, "span[class='']")[:amount]

    # product description
    descriptions = driver.find_elements(By.CSS_SELECTOR, "p[style^='-webkit-line-cla']")[:amount]
    
    # product info link
    info_links = driver.find_elements(By.CSS_SELECTOR, "a[class='iva-item-sliderLink-uLz1v']")[:amount]
    info_links = [link.get_attribute('href') for link in info_links]

    # get product image
    elements = driver.find_elements(By.CSS_SELECTOR, "img[class^='photo-slider-image']")[:amount]
    img_links = []
    for element in elements:
        img_links += [element.get_attribute('src')]
    
    products = []
    for i in range(amount):
        product = Product(info_links[i], img_links[i], prices[i].text, descriptions[i].text, names[i].text)
        products += [product]
    # img_link = element.get_attribute('src')

    # responce = requests.get(img_link, stream=True)
    # with open(Path(__file__).parent / 'product_image.jpg', 'wb') as img:
    #     shutil.copyfileobj(responce.raw, img)
    # del responce

    # driver.current_url
    driver.close()

    return products


if __name__ == '__main__':
    products = get_avito_products('kid', _filter='cheaper')
    print(str(products[0]))