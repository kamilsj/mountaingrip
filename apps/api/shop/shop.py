from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class AddProduct(APIView):
    pass

class ShowProduct(APIView):
    pass

class IndexProduct(APIView):
    pass