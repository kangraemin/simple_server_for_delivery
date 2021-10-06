from rest_framework import serializers
from .models import Restaurants
from foods.models import SubFoodCategory, MainFoodCategory


class SearchRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = (
            "id",
            "name",
            "lat",
            "lng",
            "full_address",
        )
        read_only_fields = (
            "id",
            "name",
            "lat",
            "lng",
            "full_address",
        )


class RestaurantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = "__all__"
