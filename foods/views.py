from rest_framework.permissions import IsAdminUser
from config.views import APIKeyModelViewSet
from .models import MainFoodCategory, SubFoodCategory
from .serializers import MainFoodCategorySerializer, SubFoodCategorySerializer


class MainFoodViewSet(APIKeyModelViewSet):

    queryset = MainFoodCategory.objects.all()
    serializer_class = MainFoodCategorySerializer

    def get_permissions(self):
        return [IsAdminUser]


class SubFoodViewSet(APIKeyModelViewSet):

    queryset = SubFoodCategory.objects.all()
    serializer_class = SubFoodCategorySerializer

    def get_permissions(self):
        return [IsAdminUser]
