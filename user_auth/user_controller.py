from django.utils import timezone
from django.contrib.auth import authenticate

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
        
