from datetime import timezone
from django.db import models
from user_auth.models import User

# Create your models here.  release_date = models.DateField()

class Payments(models.Model):
    payment_type = models.CharField(max_length=50)
    price = models.PositiveBigIntegerField()
    worker_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='worker_user1', null=True, blank=True)



class Orders(models.Model):

    total_price = models.PositiveBigIntegerField()
    delivered_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    worker_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='worker_user2', null=True, blank=True)
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='customer_user', null=True, blank=True)
    payments = models.OneToOneField(Payments, on_delete=models.CASCADE,related_name='fff', null=True, blank=True)
    
     

class Products(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.PositiveIntegerField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='added_by_user', null=True, blank=True)
    orders = models.ManyToManyField(Orders, related_name='kkk', null=True, blank=True)
