from pathlib import Path
from requests import get
from shutil import copyfileobj, rmtree


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

def download_images(products: list[Product]):
    image_folder_location = Path(__file__).parent / 'Product images'

    # if image_folder_location.exists():
    #     rmtree(image_folder_location)
    image_folder_location.mkdir(exist_ok=True)

    for i, product in enumerate(products):
        responce = get(product.img_path, stream=True)
        with open(image_folder_location / f'product_{i}.jpg', 'wb') as img:
            copyfileobj(responce.raw, img)
        del responce