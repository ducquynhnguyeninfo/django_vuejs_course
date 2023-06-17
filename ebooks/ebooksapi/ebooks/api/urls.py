from django.urls import path
from .views import EbookListCreateApiView, EbookDetailApiView, ReviewCreateApiView, ReviewDetailApiView


urlpatterns = [
    path("ebooks/", EbookListCreateApiView.as_view(), name="ebook-list"),
    path("ebooks/<int:pk>", EbookDetailApiView.as_view(), name="ebook-detail"),
    path("ebooks/<int:ebook_pk>/reviews/", ReviewCreateApiView.as_view(), name="ebook-review"),
    path("reviews/<int:pk>", ReviewDetailApiView.as_view(), name="review-detail"),
]
