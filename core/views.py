from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_api_key.permissions import HasAPIKey

# Create your views here.
def home(request):
    return render(request, "home.html")


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)


class APIKeyModelViewSet(ModelViewSet):
    def get_base_permission(self):
        return [HasAPIKey]
