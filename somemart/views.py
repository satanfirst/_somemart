import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from marshmallow import Schema, fields
from marshmallow.validate import Length, Range
from .models import Item, Review


class ReviewSchema(Schema):
    title = fields.Str(validate=Length(1, 64))
    description = fields.Str(validate=Length(1, 1024))
    price = fields.Int(validate=Range(min=1, max=1000000))


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        document = json.loads(request.body)
        schema = ReviewSchema()
        data = schema.loads(document)
        return JsonResponse(data, status=201)


class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        # Здесь должен быть ваш код
        return JsonResponse(status=201)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        # Здесь должен быть ваш код
        return JsonResponse(status=200)
