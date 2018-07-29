from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import SignUpForm, ConnectionForm

#from django.http import HttpResponse
#from django.template import loader

def home_page(request):
    return render(request, 'substitution_app/home_page.html')
    #template = loader.get_template('substitution_app/home_page.html')
    #return HttpResponse(template.render(request=request))

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