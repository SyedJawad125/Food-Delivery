from django.shortcuts import render

from django.shortcuts import render
from . models import Orders,Payments,Products
from django.shortcuts import render,HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
#from .blog_serializer import BlogSerializer
from utils.base_authentication import JWTAuthentication
from .food_controller import PaymentsController, OrdersController, ProductsController


payments_controller = PaymentsController()
orders_controller = OrdersController()
products_controller = ProductsController()
# Create your views here.

class PaymentsViews(ModelViewSet):
    authentication_classes = [JWTAuthentication]

    def post_payments(self, request):
        return payments_controller.create(request)
    
    def get_payments(self, request):
        return payments_controller.get_payments(request)
    
    def update_payments(self, request):
        return payments_controller.update_payments(request)
    
    def delete_payments(self, request):
        return payments_controller.delete_payments(request)
    
class OrdersViews(ModelViewSet):
    authentication_classes = [JWTAuthentication]

    def post_orders(self, request):
        return orders_controller.create(request)
    
    def get_orders(self, request):
        return orders_controller.get_orders(request)
    
    def update_orders(self, request):
        return orders_controller.update_orders(request)
    
    def delete_orders(self, request):
        return orders_controller.delete_orders(request)
    

class ProductsViews(ModelViewSet):
    authentication_classes = [JWTAuthentication]

    def post_products(self, request):
        return products_controller.create(request)
    
    def get_products(self, request):
        return products_controller.get_products(request)
    
    def update_products(self, request):
        return products_controller.update_products(request)
    
    def delete_products(self, request):
        return products_controller.delete_products(request)
    
