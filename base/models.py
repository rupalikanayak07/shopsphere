from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class product(models.Model):
    pname=models.CharField(max_length=100)
    pdesc=models.CharField(max_length=200)
    price=models.IntegerField()
    pcategory=models.CharField(max_length=100)
    trending=models.BooleanField(default=False)
    offer=models.BooleanField(default=False)
    pimages=models.ImageField(default='default.jpg',upload_to='uploads')


class cartmodel(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    pname=models.CharField(max_length=100)
    price=models.IntegerField()
    pcategory=models.CharField(max_length=100)
    quantity=models.IntegerField()
    totalprice=models.IntegerField()
    host=models.ForeignKey(User,on_delete=models.CASCADE)



class Order(models.Model):
    STATUS_CHOICES = [
        ('Placed', 'Placed'),
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    total_amount = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Placed')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(product, on_delete=models.CASCADE)

    pname = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    totalprice = models.IntegerField()

    def __str__(self):
        return self.pname