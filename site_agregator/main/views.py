from django.shortcuts import render
from django.http import HttpResponse
from main.sites.avito import get_avito_products
from main.product.product import Product
from pprint import pprint


def index(request) -> HttpResponse:
    if request.method == 'POST' and request.POST['search']:
        query = request.POST['search']
        products = get_avito_products(query, _filter='cheaper')
    else: products = [Product()]
    return render(request, 'main/index.html', {'products' : products})