from main.sites.product import Product
from main.sites.site import Site


def get_products(url: str, product_name: str, elements_pattern: list[str]) -> list[Product]:
    elements_name = ['search', 'search_btn', 'name', 'price', 'description', 'image_link', 'info_link'] 

    site = Site()
    site.search(url, product_name, elements_name, elements_pattern)

    return site.products
