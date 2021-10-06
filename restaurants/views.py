import operator
import functools
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, renderer_classes
from core.views import APIKeyModelViewSet
from .serializers import (
    RestaurantsSerializer,
    SearchRestaurantSerializer,
)
from .models import Restaurants
from .renderers import QuerySearchResultRenderer
from .errors import RestaurantAPIError
from logs.models import UserSearchLog
from foods.models import MainFoodCategory, SubFoodCategory
from videos.models import YoutubeVideo


class RestaurantViewSet(APIKeyModelViewSet):

    queryset = Restaurants.objects.all()
    serializer_class = RestaurantsSerializer

    def get_permissions(self):
        permission_classes = self.get_base_permission()
        if self.action == "retrieve" or self.action == "query_search":
            permission_classes += [permissions.AllowAny]
        # If case for update / delete ... is able only admin
        # If owner want to modify this, they have to send proposals of modifications to admin users
        else:
            permission_classes += [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    @renderer_classes(QuerySearchResultRenderer)
    def query_search(self, request):
        query = request.GET.get("query", None)
        page = request.GET.get("page", 1)
        page_size = settings.DEFAULT_PAGE_SIZE

        if not query:
            return Response(
                {str(RestaurantAPIError.SEARCH_RESTAURANT_EMPTY_QUERY_INFO)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        raw_query = query
        region_query = []
        food_query = []
        split_query = query.split()
        for query in split_query:
            count_list = []
            count_list.append(
                Restaurants.objects.filter(
                    Q(full_address__icontains=query)
                    | Q(province__icontains=query)
                    | Q(district__icontains=query)
                    | Q(old_district__icontains=query)
                ).count()
            )
            count_list.append(
                (
                    MainFoodCategory.objects.filter(Q(name__icontains=query)).count()
                    + SubFoodCategory.objects.filter(Q(name__icontains=query)).count()
                )
            )

            max_val = count_list.index(max(count_list))
            if max_val == 0:
                region_query.append(query)
            else:
                food_query.append(query)

        if not request.user.is_anonymous:
            user_search_log = UserSearchLog.objects.create(
                search_keyword=raw_query, user=request.user
            )
        else:
            user_search_log = UserSearchLog.objects.create(search_keyword=raw_query)
        if food_query:
            user_search_log.food_keyword = str(food_query)
        if region_query:
            user_search_log.region_keyword = str(region_query)
        user_search_log.save()

        try:
            main_food_category = MainFoodCategory.objects.filter(
                functools.reduce(
                    operator.or_, (Q(name__icontains=x) for x in food_query)
                )
            )
        except Exception:
            main_food_category = MainFoodCategory.objects.all()
        try:
            sub_food_category = SubFoodCategory.objects.filter(
                functools.reduce(
                    operator.or_, (Q(name__icontains=x) for x in food_query)
                )
            )
        except Exception:
            sub_food_category = SubFoodCategory.objects.all()

        try:
            restaurant = Restaurants.objects.filter(
                functools.reduce(
                    operator.or_, (Q(name__icontains=x) for x in region_query)
                )
                | functools.reduce(
                    operator.or_, (Q(full_address__icontains=x) for x in region_query)
                )
                | functools.reduce(
                    operator.or_, (Q(province__icontains=x) for x in region_query)
                )
                | functools.reduce(
                    operator.or_, (Q(district__icontains=x) for x in region_query)
                )
                | functools.reduce(
                    operator.or_, (Q(old_district__icontains=x) for x in region_query)
                )
            )
        except Exception:
            restaurant = Restaurants.objects.all()

        if len(split_query) == 1:
            if food_query:
                youtube_videos = YoutubeVideo.objects.filter(
                    Q(main_food_category__id__in=main_food_category.values_list("id"))
                    | Q(sub_food_category__id__in=sub_food_category.values_list("id"))
                ).distinct()
            else:
                youtube_videos = YoutubeVideo.objects.filter(
                    Q(restaurant__id__in=restaurant.values_list("id"))
                ).distinct()
        else:
            youtube_videos = YoutubeVideo.objects.filter(
                (
                    Q(main_food_category__id__in=main_food_category.values_list("id"))
                    | Q(sub_food_category__id__in=sub_food_category.values_list("id"))
                )
                & Q(restaurant__id__in=restaurant.values_list("id"))
            ).distinct()

        result_restaurant = Restaurants.objects.filter(
            id__in=youtube_videos.values_list("restaurant")
        ).distinct()

        paginator = Paginator(result_restaurant, page_size)
        try:
            page = paginator.validate_number(page)
            result_restaurant = paginator.get_page(page)
        except EmptyPage:
            result_restaurant = Restaurants.objects.none()

        restaurant_serializer = SearchRestaurantSerializer(
            result_restaurant, many=True, context={"request": request}
        )
        response_dict = {"restaurants": restaurant_serializer.data}
        return Response(response_dict)
