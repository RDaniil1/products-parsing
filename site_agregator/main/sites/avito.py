from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from main.product.product import Product, download_images
from time import sleep


def get_text_from_elements(driver, css_selector: str, amount: int) -> list[str]:
    elements = driver.find_elements(By.CSS_SELECTOR, css_selector)[:amount]
    match css_selector:
        case "img[class^='styles-extended-gallery-img']":
            return [element.get_attribute('src') for element in elements]
        case "a[class='iva-item-sliderLink-uLz1v']":
            return [element.get_attribute('href') for element in elements]
        case _:
            return [element.text for element in elements]

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
    
    driver = Firefox(options=firefox_options)
    url = f'{base_url}/{town}?q={product_name}&s={_filter}'
    driver.get(url)

    # product item 
    # driver.find_element(By.CSS_SELECTOR, "div[class^='iva-item-root-']").click()

    # element_dispatcher = {
    #     'name' : "h3[class^='styles-module-root-TWVKW']",
    #     'price' : "span[class='']",
    #     'description' : "p[style^='-webkit-line-cla']",
    #     'info_link' : "a[class='iva-item-sliderLink-uLz1v']",
    #     'image_link' : "img[class^='photo-slider-image']"
    # }

    # for element, pattern in element_dispatcher:
    #     if element not in ['image_link', 'info_link']:
    #         driver.find_elements(By.CSS_SELECTOR, pattern)[:amount]

    # product name
    names = get_text_from_elements(driver, "h3[class^='styles-module-root-TWVKW']", amount)

    # product price
    prices = get_text_from_elements(driver, "span[class='']", amount)

    # product description
    descriptions = get_text_from_elements(driver, "p[style^='-webkit-line-cla']", amount)
    
    # product info link
    info_links = get_text_from_elements(driver, "a[class='iva-item-sliderLink-uLz1v']", amount)

    image_links = []
    for info in info_links:
        driver.get(info)
        sleep(2)

        driver.find_element(By.CSS_SELECTOR, "div[class='gallery-block-itemViewGallery-_Pfeg']").click()

        # get product image
        image_links += get_text_from_elements(driver, "img[class^='styles-extended-gallery-img']", amount)
    
    desc_size = 150
    products = []
    for i in range(amount):
        product = Product(info_links[i], image_links[i], prices[i], descriptions[i][:desc_size], names[i])
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
    query = 'switch'
    products = get_avito_products(query, _filter='cheaper')
    
    # download_images(products)

    # print(str(products[0]))