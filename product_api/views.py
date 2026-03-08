from django.shortcuts import render
from django.http import HttpResponse
from base.models import product
from .serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework import status

# Create your views here.
def all_products(request):
    products=product.objects.all()
    python_serialized_data=ProductSerializer(products,many=True)
    python_data=python_serialized_data.data
    json_data=JSONRenderer().render(python_data)
    return HttpResponse(json_data)




def cart_data(request):
    if request.method == 'POST':
        req_data=request.body
        de_ser=CartSerializer(data=req_data)
        if de_ser.is_valid():
            de_ser.create()
            return HttpResponse(status=status.HTTP_201_CREATED)