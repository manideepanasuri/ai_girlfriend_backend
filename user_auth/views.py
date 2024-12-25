from django.template.context_processors import request
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *




class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, request, *args, **kwargs):
        # Call the superclass's create method to create the user
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(id=response.data['id'])  # Get the created user instance
        token_data = MyTokenObtainPairSerializer.get_token(user)
        tokens = {
            'refresh': str(token_data),
            'access': str(token_data.access_token),
        }  # Generate tokens for the user

        # Add tokens to the response data
        return Response(
            {**tokens},
            status=status.HTTP_201_CREATED
        )






