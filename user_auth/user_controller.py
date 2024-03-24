from urllib import response
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.response import Response
from user_auth.user_serializer import *
from user_auth.models import Token, User
from utils.reusable_methods import get_first_error_message, generate_six_length_random_number
from utils.response_messages import *
from utils.helper import create_response, paginate_data


class ChangePasswordController:
    serializer_class = ChangePasswordSerializer
    def change_password(self,request):
        try:
            user = request.user
            if not user:
                return create_response({},USER_NOT_FOUND, status_code=400)

            serialized_data = self.serializer_class(data=request.data, context={'user':user})

            if serialized_data.is_valid():
                user.set_password(request.data['new_password'])
                user.save()
                return create_response({},PASSWORD_UPDATED, status_code=200)
            else:
                return create_response({},get_first_error_message(serialized_data.errors, UNSUCCESSFUL), status_code=400)
        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)


class RegisterController:
    serializer_class = UserSerializer
    def create(self,request):
        try:
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid():
                instance = serialized_data.save()
                return create_response(self.serializer_class(instance).data, SUCCESSFUL, status_code=200)
            else:
                return create_response({}, get_first_error_message(serialized_data.errors, UNSUCCESSFUL), status_code=400)
        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)



        
class LoginController:
    serializer_class = LoginSerializer

    def login(self, request):
        try:
            serialized_data = self.serializer_class(data=request.data)

            if not serialized_data.is_valid():
                return create_response({},get_first_error_message(serialized_data.errors, UNSUCCESSFUL), 400)

            user = authenticate(username=request.data['username'], password=request.data['password'])
            if not user:
                return create_response({}, message=INCORRECT_EMAIL_OR_PASSWORD, status_code=400)

            response_data = {
                "guid":user.guid,
                "token": user.get_access_token(),
                "name": user.get_full_name(),
                "username":user.username,
                "email": user.email
            }

            Token.objects.update_or_create(defaults={"token": response_data.get("token")},user_id=user.guid)
            user.failed_login_attempts = 0
            user.last_failed_time = None
            user.last_login = timezone.now()
            user.save()
            return create_response(response_data, SUCCESSFUL, status_code=200)
        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)
        

class LogoutController:
    def logout(self,request):
        try:
            user = request.user.guid
            token = Token.objects.filter(user=user)
            if not token:
                return create_response({},UNSUCCESSFUL, status_code=400)
            token.delete()
            return create_response({}, SUCCESSFUL, status_code=200)
        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)
        

class UserListingController:
    def get_user(self, request):
        try:
            kwargs = {}
            guid = request.query_params.get('guid', None)
            username = request.query_params.get('username', None)
            first_name = request.query_params.get('first_name', None)
            last_name = request.query_params.get('last_name', None)
            address = request.query_params.get('address', None)
            
            if guid:
                kwargs['guid'] = guid
            if username:
                kwargs['username'] = username
            if first_name:
                kwargs['first_name__icontains'] = first_name
            if last_name:
                kwargs['last_name__icontains'] = last_name
            if address:
                kwargs['address__icontains'] = address

            instances = User.objects.filter(**kwargs)
            serialized_instances = UserSerializer(instances, many=True).data
            response_data = {
                "count": instances.count(),
                "data": serialized_instances
            }
            return Response(response_data, 200)
        except Exception as e:
            return Response({'error':str(e)}, 500)
            
    # def get_courses(self, request):
    #     instances = Courses.objects.all()
    #     response_data = CoursesSerializer(instances, many=True).data
    #     print(instances)
    #     print(response_data)
    #     return Response({"data":response_data}, 200)
        

    # class YourModelAPIView(APIView):
    #     def get(self, request):
    #         queryset = YourModel.objects.all()
    #         serializer = YourModelSerializer(queryset, many=True)
    #         return Response(serializer.data)
        

        # try:
        #     kwargs = {}
        #     id = request.query_params.get('id', None)
        #     payment_type = request.query_params.get('payment_type', None)
        #     price = request.query_params.get('price', None)
        #     date_to = request.query_params.get('date_to', None)
        #     date_from = request.query_params.get('date_from', None)
        #     date = request.query_params.get('date', None)

        #     if id:
        #         kwargs['id'] = id
        #     if payment_type:
        #         kwargs['name__icontains'] = payment_type
        #     if price:
        #         kwargs['price'] = price
        #     if date:
        #         kwargs['created_at__date'] = date
        #     if date_from:
        #         kwargs['created_at__date__gte'] = date_from
        #     if date_to:
        #         kwargs['created_at__date__lte'] = date_to

        #     instances = Payments.objects.filter(**kwargs)
        #     serialized_instances = PaymentsSerializer(instances, many=True).data