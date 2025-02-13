import jwt
from django.conf import settings
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, LoginSerializer, UserUpdateSerializer
from .utils import json_response
from .models import CustomUser

200 == status.HTTP_200_OK
201 == status.HTTP_201_CREATED,
400 == status.HTTP_400_BAD_REQUEST
403 == status.HTTP_403_FORBIDDEN
404 == status.HTTP_404_NOT_FOUND
500 == status.HTTP_500_INTERNAL_SERVER_ERROR

class AuthViewSet(ViewSet):
    
    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def register(self, request):
        token = request.data.get("token")
        if not token:
            return json_response(data=None, message='Token Not Provided', error=True, status=400)

        try:
            token_payload = jwt.decode(token, settings.TOKEN_KEY, algorithms=["HS256"])
            verified_email = token_payload.get("email")
            if not verified_email:
                return json_response(data=None, message='Email Verification Failed.', error=True, status=400)

            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                if serializer.validated_data.get("email") != verified_email:
                    return json_response(
                        data=None, message='Email mismatch. The provided email does not match the verified email.',
                        error=True,
                        status=400
                    )
                user = serializer.save()
                return json_response(
                    data={
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                    message='User created successfully.',
                    status=201
                )
            return json_response(data=None, message=serializer.errors, error=True, status=400)

        except jwt.ExpiredSignatureError:
            return json_response(data=None, message="Token has expired", error=True, status=400)
        except jwt.DecodeError:
            return json_response(data=None, message='Invalid token', error=True, status=400)
        
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data.get("user")

            if not user:
                return json_response(data=None, message='User authentication failed.', error=True, status=404)

            try:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)  
                refresh_token = str(refresh)           
                return json_response(data= {
                    "email": user.email,
                    "user_id": user.id,
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }, message="User logged in successfully.", error=False, status=200)

            except Exception as token_error:
                return json_response(data=None, message= f"Token creation error: {str(token_error)}", status=500)

        return json_response(message=serializer.errors, status=400)
    
    @action(detail=False, methods=["put"], permission_classes=[IsAuthenticated])
    def update_user(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return json_response(data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                }, 
                message= "User information updated successfully",
                error=False, status=200)

        return json_response(data=None, message=serializer.errors, error=True, status=400)
    
    @action(detail=False, methods=["delete"], permission_classes=[IsAdminUser])
    def delete_account(self, request):
        user_id = request.query_params.get("user_id")

        if not user_id:
            return json_response(message= "User ID is required.", error=True, status=400)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return json_response(message = "User not found.", error=True, status=404)

        if request.user.id == user.id:
            return json_response(message= "You cannot delete your own account.", error=True, status=403)

        user.delete()
        return json_response(message = "User account deleted successfully.", status=200)