from django.urls import path
from .views import PaymentsViews, OrdersViews, ProductsViews

urlpatterns=[
    path('payments', PaymentsViews.as_view({"get":"get_payments",
                            "post":"post_payments",
                            "patch":"update_payments",
                            "delete":"delete_payments"})),

    path('orders', OrdersViews.as_view({"get":"get_orders",
                            "post":"post_orders",
                            "patch":"update_orders",
                            "delete":"delete_orders"})),

    path('products', ProductsViews.as_view({"get":"get_products",
                            "post":"post_products",
                            "patch":"update_products",
                            "delete":"delete_products"})),

     
    path('products/aggregation', ProductsViews.as_view({"get":"products_aggregation"})),

    path('products/annotation', ProductsViews.as_view({"get": "products_annotation"})),

    #path('products/aggregation/', ProductsViews.as_view(), name='product-aggregation'),

]