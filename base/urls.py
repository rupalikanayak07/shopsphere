from django.urls import path
from .views import *


urlpatterns=[
    path('',home,name='home'),
    path('addtocart/<int:pk>',addtocart,name='addtocart'),
    path('cart/',cart,name='cart'),
    path('remove/<int:pk>',remove,name='remove'),
    path('decrease/<int:pk>',decrease,name='decrease'),
    path('increase/<int:pk>',increase,name='increase'),
    path('details/',details,name='details'),
    path('orderplaced/',orderplaced,name='orderplaced'),
    path('orderhistory/',orderhistory,name='orderhistory'),
]