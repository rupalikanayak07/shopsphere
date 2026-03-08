from rest_framework import serializers
from base.models import cartmodel
from django.contrib.auth.models import User


class ProductSerializer(serializers.Serializer):
    pname = serializers.CharField(max_length=100)
    pdesc = serializers.CharField(max_length=200)
    price = serializers.IntegerField(default=0)
    pcategory = serializers.CharField(max_length=50)
    trending = serializers.BooleanField(default=False)
    offer = serializers.BooleanField(default=False)
    pimages = serializers.ImageField(default='uploads/Default.jpg', required=False)



class CartSerializer(serializers.Serializer):
    pname = serializers.CharField(max_length=100)
    price = serializers.IntegerField(default=0)
    pcategory = serializers.CharField(max_length=50)
    quantity = serializers.IntegerField(default=1)
    totalprice = serializers.IntegerField(default=0)
    host = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['host'] = user
        return cartmodel.objects.create(**validated_data)
