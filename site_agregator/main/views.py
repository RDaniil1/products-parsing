from django.shortcuts import render
from django.http import HttpResponse
from main.sites.site_parsing import get_products
from main.sites.product import Product
from pprint import pprint


def index(request) -> HttpResponse:
    if request.method == 'POST' and request.POST['search']:
        query = request.POST['search']
        url = 'https://avito.ru'
        elements_pattern = ['input[class^="styles-module-input-"]', 
                        'button[data-marker="search-form/submit-button"]',

                        'a[class^="styles-module-root"]', 
                        'strong[class="styles-module-root-LEIrw"]',
                        'p[class^="styles-module-root"]', 
                        'img[itemprop="image"]',
                        'div[data-marker="item"]']

        products = get_products(url, query, elements_pattern)
    else: products = [Product()]
    return render(request, 'main/index.html', {'products' : products})