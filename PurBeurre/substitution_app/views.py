from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404

from .forms import SignUpForm, ConnectionForm

from . import callapi



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
    if apiQuery == 404:
        raise Http404("Erreur 404")
    else:
        apiQuery = callapi.barcode_clean_the_oppenfoodfact_api_request(apiQuery)

    return render(request, 'substitution_app/results.html', {'apiQuery': apiQuery})
