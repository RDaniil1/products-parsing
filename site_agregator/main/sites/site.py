from time import sleep
from main.sites.product import Product
from main.sites.driver_options import DiverOptions

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class Site:
    def __init__(self):
        self.driver = webdriver.Firefox

        self.element_dispatcher = {}

        self.product_data: list[list[str]]

        self.amount = 5
        self.products: list[Product]

        self.product_names, self.prices, self.descriptions, self.image_lniks, self.info_links = [''] * 5
        self.product_data = []
        self.products = []

    def __del__(self):
        self.driver.close()

    def set_driver_init_data(self, url: str):
        driver_options = DiverOptions()
        driver_options.create()

        self.driver = Firefox(options=driver_options.options)
        self.driver.get(url)

    def search(self, url: str, product_name: str, elements_name: list[str], elements_pattern: list[str]):        
        self.set_driver_init_data(url)
        
        self.set_element_dispatcher(elements_name, elements_pattern)
        self.send_product_name(product_name)

        self.set_product_data(elements_name)
        self.product_names, self.prices, self.descriptions, self.image_lniks, self.info_links = self.product_data

        self.set_products()

    def set_element_dispatcher(self, elements_name: list[str], elements_pattern: list[str]):
        self.element_dispatcher = dict(zip(elements_name, elements_pattern))

    def send_product_name(self, product_name: str):
        self.driver.find_element(By.CSS_SELECTOR, self.element_dispatcher['search']).click() 
        self.driver.find_element(By.CSS_SELECTOR, self.element_dispatcher['search']).send_keys(product_name)
        self.driver.find_element(By.CSS_SELECTOR, self.element_dispatcher['search']).send_keys(Keys.ENTER)

    def get_text_from_elements(self, css_selector: str, amount: int) -> list[str]:
        elements = self.driver.find_elements(By.CSS_SELECTOR, css_selector)[:amount]
        match css_selector:
            case 'img[itemprop="image"]':
                return [element.get_attribute('src') for element in elements]
            case 'a[data-marker="item"]':
                return [element.get_attribute('href') for element in elements]
            case _:
                return [element.text for element in elements]

    def set_product_data(self, elements_name: list[str]):
        for name in elements_name:
            if name in ['name', 'price', 'description', 'image_link', 'info_link']:
                self.product_data += [self.get_text_from_elements(self.element_dispatcher[name], self.amount)]

    def set_products(self):
        desc_size = 150
        for i in range(self.amount):
            product = Product(self.info_links[i], self.image_links[i], 
                              self.prices[i], self.descriptions[i][:desc_size],
                              self.product_names[i])
            self.products += [product]