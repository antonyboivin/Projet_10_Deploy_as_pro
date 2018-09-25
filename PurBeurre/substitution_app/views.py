from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404

from .forms import SignUpForm, ConnectionForm
from .models import ProductsA, UserProducts

from . import callapi

import json

def home_page(request):
    return render(request, 'substitution_app/home_page.html')


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(home_page)
    else :
        form = SignUpForm()
    return render(request, 'substitution_app/signup.html', {'form': form})


def connection(request):
    error = False

    if request.method == "POST":
        form = ConnectionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                return render(request, 'substitution_app/home_page.html', locals()) #substitution_app/home_page.html
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnectionForm()

    return render(request, 'substitution_app/connection.html', locals())


def deconnection(request):
    logout(request)
    return redirect(reverse(home_page))


def myaccount(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, 'substitution_app/myaccount.html', {'username': username})


def product_select(request):
    if request.method == 'POST':
        userQuery = request.POST.get('userQuery')
        apiQuery = callapi.request_the_openfoodfact_api(userQuery)

        if apiQuery == 404:
            raise Http404("Erreur 404")
        else:
            apiQuery = callapi.clean_the_openfoodfact_api_request(apiQuery)

        return render(request, 'substitution_app/product_select.html', {'apiQuery': apiQuery, 'userQuery' : userQuery})


def results(request, code):
    apiQuery = callapi.barcode_request_the_openfoodfact_api(code)
    apiQuery = callapi.barcode_clean_the_oppenfoodfact_api_request(apiQuery)

    if apiQuery == 404:
        raise Http404("Erreur 404")
    else:
        categorie = apiQuery['categories_hierarchy'][0]
        substitution = ProductsA.objects.filter(main_category__contains=categorie)        
        if substitution.exists():
            return render(request, 'substitution_app/results.html', {'apiQuery': apiQuery, 'substitution': substitution})
        else:
            substitution = callapi.request_for_substitution_products_in_openfoodfact_api(apiQuery)
            substitution = callapi.clean_substitution_products_in_openfoodfact_api(substitution)

            return render(request, 'substitution_app/results.html', {'apiQuery': apiQuery, 'substitution': substitution})
    

def my_products(request):
    user_products = UserProducts.objects.all() 
    context = {
        'user_products' : user_products
    }
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            code = request.POST.get('code')
            url = request.POST.get('url')
            product_name = request.POST.get('product_name')
            nutrition_grade_fr = request.POST.get('nutrition_grade_fr')
            main_category = request.POST.get('main_category')
            main_category_fr = request.POST.get('main_category_fr')
            image_small_url = request.POST.get('image_small_url')

            return render(request, 'substitution_app/myproducts.html', context)
    else:
        if request.user.is_authenticated:
            print(request.user.username)
            return render(request, 'substitution_app/myproducts.html', context)
        else:
            return redirect(connection)


def product_display(request, code):
    apiQuery = callapi.barcode_request_the_openfoodfact_api(code)
    if apiQuery == 404:
        raise Http404("Erreur 404")
    else:
        apiQuery = callapi.barcode_clean_the_oppenfoodfact_api_request(apiQuery)

    return render(request, 'substitution_app/product_display.html', {'apiQuery': apiQuery})

"""
def my_products(request):
    if request.user.is_authenticated:
        return render(request, 'substitution_app/myproducts.html')
    else:
        return redirect(connection)


           
            products_save = UserProducts.objects.create(
                username = username,
                code = code,
                url = url,
                product_name = product_name,
                nutrition_grade_fr = nutrition_grade_fr,
                main_category = main_category,
                main_category_fr = main_category_fr,
                image_small_url = image_small_url
        )
"""


