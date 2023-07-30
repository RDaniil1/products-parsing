from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from pprint import pprint
from fake_useragent import UserAgent
import shutil
import requests
from pathlib import Path
import os
from selenium_recaptcha_solver import RecaptchaSolver

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

def get_market_products(product_name: str, amount=5) -> list[Product]:
    base_url = 'https://market.yandex.ru'

    user_agent = UserAgent()

    firefox_options = Options()
    # firefox_options.add_argument("--headless")
    firefox_options.add_argument(f'user-agent={user_agent.random}')
    firefox_options.add_argument('--proxy-server=127.0.0.1:9050')
    
    driver = Firefox(options=firefox_options)

    solver = RecaptchaSolver(driver)
    driver.get(base_url)

    captcha = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    solver.click_recaptcha_v2(captcha)

    # driver.find_element(By.CSS_SELECTOR, "input[itemprop='query-input']").send_keys(product_name)
    # driver.find_element(By.CSS_SELECTOR, "button[data-auto='search-button']").click()

    
    
    driver.close()

    return [Product()]


if __name__ == '__main__':
    products = get_market_products('samsung')
    print(str(products[0]))