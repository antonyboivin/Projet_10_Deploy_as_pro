from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

def home_page(request):
    template = loader.get_template('substitution_app/home_page.html')
    return HttpResponse(template.render(request=request))
