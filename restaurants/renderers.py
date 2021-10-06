from rest_framework.renderers import BaseRenderer
from rest_framework.utils import json


class QuerySearchResultRenderer(BaseRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_dict = {
            "restaurants": [],
        }
        if data.get("restaurants"):
            response_dict["restaurants"] = data.get("restaurants")
        data = response_dict
        return json.dumps(data)
