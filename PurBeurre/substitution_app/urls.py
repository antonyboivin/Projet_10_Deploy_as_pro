from django.urls import path
from . import views


urlpatterns = [
    path('home_page/', views.home_page, name='home page'),
    path('signup/', views.signup, name='sign up'),
    path('connection/', views.connection, name='connection'),
    path('deconnection/', views.deconnection, name='deconnection'),
    path('myaccount/', views.myaccount, name='my account'),
    path('product_select/', views.product_select, name='product select'),
    path('results/<int:code>', views.results, name='results'),
]