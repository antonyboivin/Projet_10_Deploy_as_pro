from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

def home_page(request):
    return render(request, 'substitution_app/home_page.html')
    #template = loader.get_template('substitution_app/home_page.html')
    #return HttpResponse(template.render(request=request))

def signup(request):
    pass

