from django.db import models
from core import models as core_models
from django.contrib.auth.models import User


class UserSearchLog(core_models.TimeStampedModel):
    search_keyword = models.CharField(
        max_length=200,
        blank=False,
        null=False,
    )
    user = models.ForeignKey(
        User,
        related_name="user_search_logs",
        on_delete=models.DO_NOTHING,
        null=True,
    )
    food_keyword = models.TextField(blank=True, null=True)
    region_keyword = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "user_search_log"
