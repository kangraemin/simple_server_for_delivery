from django.db import models
from core import models as core_models


class YoutubeVideo(core_models.TimeStampedModel):

    youtube_video_id = models.CharField(max_length=100, null=False, blank=False)

    main_food_category = models.ForeignKey(
        "foods.MainFoodCategory",
        related_name="youtube_videos",
        on_delete=models.PROTECT,
        null=True,
    )
    sub_food_category = models.ManyToManyField(
        "foods.SubFoodCategory",
        related_name="youtube_videos",
        through="YoutubeVideoSubCategory",
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurants",
        related_name="youtube_videos",
        on_delete=models.CASCADE,
        null=True,
    )

    youtube_video_start_time = models.IntegerField()

    class Meta:
        db_table = "youtube_video"

    def __str__(self):
        return self.pk


class YoutubeVideoSubCategory(core_models.TimeStampedModel):
    sub_food_category = models.ForeignKey(
        "foods.SubFoodCategory", on_delete=models.CASCADE
    )
    youtube_video = models.ForeignKey("YoutubeVideo", on_delete=models.CASCADE)

    class Meta:
        db_table = "youtube_video_sub_category"

    def __str__(self):
        return str(self.pk)
