# from django.urls import path
from django.conf.urls import url, include

from .views import AddItemView, GetItemView, PostReviewView

urlpatterns = [
    url('api/v1/goods/', AddItemView.as_view()),
    # path('api/v1/goods/<int:item_id>/', GetItemView.as_view()),
    # path('api/v1/goods/<int:item_id>/reviews/', PostReviewView.as_view()),
]
