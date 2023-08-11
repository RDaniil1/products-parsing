from django.shortcuts import render
from django.http import HttpResponse
from main.sites.avito import get_avito_products


def index(request):
    query = 'switch'
    products = get_avito_products(query, _filter='cheaper')
    return render(request, 'main/index.html', {'products' : products})
