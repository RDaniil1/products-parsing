from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
from product import Product
from fake_useragent import UserAgent
from proxy.random_proxies import get_random_proxy
from selenium import webdriver


def get_text_from_elements(driver, css_selector: str, amount: int) -> list[str]:
    elements = driver.find_elements(By.CSS_SELECTOR, css_selector)[:amount]
    match css_selector:
        case "img[class^='styles-extended-gallery-img']":
            return [element.get_attribute('src') for element in elements]
        case "a[class='iva-item-sliderLink-uLz1v']":
            return [element.get_attribute('href') for element in elements]
        case _:
            return [element.text for element in elements]

def get_products(url: str, product_name: str, elements_pattern: str, town='all', _filter='', amount=5) -> list[Product]:
    user_agent = UserAgent(browsers=['chrome', 'edge'])
    proxy = get_random_proxy()
    ip, port = proxy.split(':')
    
    firefox_options = Options()
    firefox_options.add_argument("--headless")

    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.socks', ip)
    profile.set_preference('network.proxy.socks_port', int(port))
    profile.set_preference("general.useragent.override", user_agent.random)
    
    driver = Firefox(options=firefox_options, firefox_profile=profile)
    driver.get(url)

    elements_name = ['search', 'search_btn', 'name', 'price', 'description', 'info_link', 'gallery', 'image_link'] 
    element_dispatcher = dict(zip(elements_name, elements_pattern))

    driver.find_element(By.CSS_SELECTOR, element_dispatcher['search']).send_keys(product_name)
    driver.find_element(By.CSS_SELECTOR, element_dispatcher['search_btn']).click()

    product_data = []
    for name in elements_name:
        if name not in ['search', 'search_btn', 'gallery', 'image_link']:
            product_data += [ get_text_from_elements(driver, element_dispatcher[name], amount) ]

    names, prices, descriptions, info_links = product_data

    image_links = []
    for info in info_links:
        driver.get(info)
        sleep(2)
        driver.find_element(By.CSS_SELECTOR, element_dispatcher['gallery']).click()
        image_links += get_text_from_elements(driver, element_dispatcher['image_link'], amount)
    
    desc_size = 150
    products = []
    for i in range(len(info_links)):
        product = Product(info_links[i], image_links[i], prices[i], descriptions[i][:desc_size], names[i])
        products += [product]

    driver.close()
    return products

if __name__ == '__main__':
    url = 'https://avito.ru'
    product_name = 'switch'
    elements_pattern = ["input[class='input-input-Zpzc1']", 
                    "button[class='desktop-8ydzks']",
                    "h3[class^='styles-module-root-TWVKW']", 
                    "span[class='']",
                    "p[style^='-webkit-line-cla']", 
                    "a[class='iva-item-sliderLink-uLz1v']", 
                    "div[class='gallery-block-itemViewGallery-_Pfeg']", 
                    "img[class^='styles-extended-gallery-img']"]
    
    products = get_products(url, product_name, elements_pattern)
    
    print(products)
