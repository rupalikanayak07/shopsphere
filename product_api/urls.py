from django.urls import path
from .views import *

urlpatterns=[
    path('all_products',all_products,name='all_products'),

    path('cart_data',cart_data,name='cart_data')
]