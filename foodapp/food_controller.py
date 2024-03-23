from django.utils import timezone
from django.contrib.auth import authenticate
from foodapp.food_serializer import *
from foodapp.models import Payments, Orders, Products
from utils.reusable_methods import get_first_error_message, generate_six_length_random_number
from rest_framework.response import Response
# from vehicle.serializer import serializer


class PaymentsController:

    def create(self, request):
        try:
            request.POST._mutable = True
            request.data["worker_user"] = request.user.guid
            request.POST._mutable = False

            validated_data = PaymentsSerializer(data=request.data)
            if validated_data.is_valid():
                response = validated_data.save()
                response_data = PaymentsSerializer(response).data
                return Response({'data':response_data} , 200)
            else:
                error_message = get_first_error_message(validated_data.errors, "UNSUCCESSFUL")
                return Response({'data':error_message}, 400)
            
        except Exception as e:
            return Response({'error':str(e)}, 500)
    
#mydata = Member.objects.filter(firstname__endswith='s').values()
    def get_payments(self, request):
        try:
            kwargs = {}
            id = request.query_params.get('id', None)
            payment_type = request.query_params.get('payment_type', None)
            price = request.query_params.get('price', None)
            date_to = request.query_params.get('date_to', None)
            date_from = request.query_params.get('date_from', None)
            date = request.query_params.get('date', None)

            if id:
                kwargs['id'] = id
            if payment_type:
                kwargs['name__icontains'] = payment_type
            if price:
                kwargs['price'] = price
            if date:
                kwargs['created_at__date'] = date
            if date_from:
                kwargs['created_at__date__gte'] = date_from
            if date_to:
                kwargs['created_at__date__lte'] = date_to

            instances = Payments.objects.filter(**kwargs)
            serialized_instances = PaymentsSerializer(instances, many=True).data

            response_data = {
                "count": instances.count(),
                "data": serialized_instances
            }

            return Response(response_data, 200)
        
        except Exception as e:
            return Response({'error':str(e)}, 500)
    
    
    def update_payments(self, request):
        try:
            if "id" in request.data:
                #finding instance
                instance = Payments.objects.filter(id=request.data["id"]).first()

                if instance:
                    # updating the instance/record
                    serialized_data = PaymentsSerializer(instance, data=request.data, partial=True)

                    if serialized_data.is_valid():
                        response = serialized_data.save()
                        response_data = PaymentsSerializer(response).data
                        return Response({"data":response_data}, 200)
                    else:
                        error_message = get_first_error_message(validated_data.errors, "UNSUCCESSFUL")
                        return Response({'data':error_message}, 400)
                    
                else:
                    return Response({"data":"NOT FOUND"}, 404)
            else:
                return Response({"data":"ID NOT PROVIDED"}, 400)
            
        except Exception as e:
            return Response({'error':str(e)}, 500)

    def delete_payments(self, request):
        try:
            if "id" in request.query_params:
                instance = Payments.objects.filter(id=request.query_params['id']).first()

                if instance:
                    instance.delete()
                    return Response({"data":"SUCESSFULL"}, 200)
                else:
                    return Response({"data":"RECORD NOT FOUND"}, 404) 
            else:
                return Response({"data":"ID NOT PROVIDED"}, 400)
        except Exception as e:
            return Response({'error':str(e)}, 500)


class OrdersController:

    def create(self, request):
        try:
            request.POST._mutable = True
            request.data["customer_user"] = request.user.guid
            request.POST._mutable = False

            validated_data = OrdersSerializer(data=request.data)
            if validated_data.is_valid():
                response = validated_data.save()
                response_data = OrdersSerializer(response).data
                return Response({'data':response_data} , 200)
            else:
                error_message = get_first_error_message(validated_data.errors, "UNSUCCESSFUL")
                return Response({'data':error_message}, 400)
            
            
        except Exception as e:
            return Response({'data': str(e)}, 500)
    
#mydata = Member.objects.filter(firstname__endswith='s').values()
    def get_orders(self, request):
        try:
            kwargs = {}
            id = request.query_params.get('id', None)
            name = request.query_params.get('name', None)
            end_name = request.query_params.get('end_name', None)
            date_to = request.query_params.get('date_to', None)
            date_from = request.query_params.get('date_from', None)
            date = request.query_params.get('date', None)
            total_price = request.query_params.get('total_price', None)

            if id:
                kwargs['id'] = id
            if total_price:
                kwargs['total_price'] = total_price
            if date:
                kwargs['delivered_at__date'] = date
            if date_from:
                kwargs['delivered_at__date__gte'] = date_from
            if date_to:
                kwargs['delivered_at__date__lte'] = date_to

            instances = Orders.objects.filter(**kwargs)
            serialized_instances = OrdersSerializer(instances, many=True).data

            response_data = {
                "count": instances.count(),
                "data": serialized_instances
            }

            return Response(response_data, 200)
        
        except Exception as e:
            return Response({'error':str(e)}, 500)
    
    
    def update_orders(self, request):
        try:
            if "id" in request.data:
                #finding instance
                instance = Orders.objects.filter(id=request.data["id"]).first()

                if instance:
                    # updating the instance/record
                    serialized_data = OrdersSerializer(instance, data=request.data, partial=True)

                    if serialized_data.is_valid():
                        response = serialized_data.save()
                        response_data = OrdersSerializer(response).data
                        return Response({"data":response_data}, 200)
                    else:
                        error_message = get_first_error_message(serialized_data.errors, 400)
                        return Response({"data":error_message}, 400)
                else:
                    return Response({"data":"NOT FOUND"}, 404)
            else:
                return Response({"data":"ID NOT PROVIDED"}, 400)
            
        except Exception as e:
            return Response({'data':str(e)}, 500)


    def delete_orders(self, request):
        try:
            if "id" in request.query_params:
                instance = Orders.objects.filter(id=request.query_params['id']).first()

                if instance:
                    instance.delete()
                    return Response({"data":"SUCESSFULL"}, 200)
                else:
                    return Response({"data":"RECORD NOT FOUND"}, 404) 
            else:
                return Response({"data":"ID NOT PROVIDED"}, 400)
            
        except Exception as e:
            return Response({'error':str(e)}, 500)    



class ProductsController:

    def create(self, request):
        try:
            request.POST._mutable = True
            request.data["added_by"] = request.user.guid
            request.POST._mutable = False

            validated_data = ProductsSerializer(data=request.data)
            if validated_data.is_valid():
                response = validated_data.save()
                response_data = ProductsSerializer(response).data
                return Response({'data':response_data} , 200)
            else:
                error_message = get_first_error_message(validated_data.errors, "UNSUCCESSFUL")
                return Response({'data':error_message}, 400)
        except Exception as e:
            return Response({'data': str(e)}, 500)
    
#mydata = Member.objects.filter(firstname__endswith='s').values()
    def get_products(self, request):
        try:
            kwargs = {}
            id = request.query_params.get('id', None)
            name = request.query_params.get('name', None)
            description = request.query_params.get('description', None)
            price =  request.query_params.get('price', None)
            end_name = request.query_params.get('end_name', None)
            date_to = request.query_params.get('date_to', None)
            date_from = request.query_params.get('date_from', None)
            date = request.query_params.get('date', None)

            if id:
                kwargs['id'] = id
            if name:
                kwargs['name__icontains'] = name
            if description:
                kwargs['description'] = description
            if price:
                kwargs['price'] = price
            if end_name:
                kwargs['name__endswith'] = end_name
            if date:
                kwargs['created_at__date'] = date
            if date_from:
                kwargs['created_at__date__gte'] = date_from
            if date_to:
                kwargs['created_at__date__lte'] = date_to

            instances = Products.objects.filter(**kwargs)
            serialized_instances = ProductsSerializer(instances, many=True).data

            response_data = {
                "count": instances.count(),
                "data": serialized_instances
            }

            return Response(response_data, 200)
        
        except Exception as e:
            return Response({'error':str(e)}, 500)
    

    def update_products(self, request):
        try:
            if "id" in request.data:
                #finding instance
                instance = Products.objects.filter(id=request.data["id"]).first()

                if instance:
                    # updating the instance/record
                    serialized_data = ProductsSerializer(instance, data=request.data, partial=True)

                    if serialized_data.is_valid():
                        response = serialized_data.save()
                        response_data = ProductsSerializer(response).data
                        return Response({"data":response_data}, 200)
                    else:
                        error_message = get_first_error_message(serialized_data.errors, 400)
                        return Response({"data":error_message}, 400)
                else:
                    return Response({"data":"NOT FOUND"}, 404)
            else:
                return Response({"data":"ID NOT PROVIDED"}, 400)

        except Exception as e:
            return Response({'data':str(e)}, 500)


    def delete_products(self, request):
        try: 
            if "id" in request.query_params:
                instance = Products.objects.filter(id=request.query_params['id']).first()

                if instance:
                    instance.delete()
                    return Response({"data":"SUCESSFULL"}, 200)
                else:
                    return Response({"data":"RECORD NOT FOUND"}, 404) 
            else:
                return Response({"data":"ID NOT PROVIDED"}, 400)
            
        except Exception as e:
            return Response({'data':str(e)}, 500)