import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Length, Range
from .models import Item, Review


class ItemSchema(Schema):
    title = fields.Str(required=True, validate=Length(min=1, max=36))
    description = fields.Str(required=True, validate=Length(min=1, max=1024))
    price = fields.Int(required=True, validate=Range(min=1, max=1000000))


class ReviewSchema(Schema):
    text = fields.Str(required=True, validate=Length(min=1, max=1024))
    grade = fields.Int(required=True, validate=Range(min=1, max=10))


# allow_none=True


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        try:
            data = json.loads(request.body)
            schema = ItemSchema(strict=True)
            schema.validate(data=data)
            new_item = Item.objects.create(title=data["title"], description=data["description"],
                                           price=data["price"])
            new_item.save()
            resp = {"id": new_item.id}
            return JsonResponse(resp, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            data = json.loads(request.body)
            schema = ReviewSchema(strict=True)
            schema.validate(data=data)
            item = Item.objects.get(id=item_id)
            new_review = Review.objects.create(text=data["text"], grade=data["grade"],
                                               item=item)
            new_review.save()
            resp = {"id": new_review.id}
            return JsonResponse(resp, status=201)
        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            reviews = Review.objects.filter(item_id=item_id)
            f_reviews = sorted([dict(id=x.id, text=x.text, grade=x.grade) for x in reviews][-5:], key=lambda x: x['id'],
                               reverse=True)
            resp = dict(id=item.id, title=item.title, description=item.description,
                        price=item.price, reviews=f_reviews)
            return JsonResponse(resp, status=200)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, status=404)
