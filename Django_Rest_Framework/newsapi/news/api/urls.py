from django.urls import path
# from news.api.views import article_list_create_api_view, article_detail_api_view
from news.api.views import ArticleListApiView, ArticleDetailApiView
from news.api.views import JournalistListApiView

urlpatterns = [
    # path("articles/", article_list_create_api_view, name="article-list"),
    # path("articles/<int:pk>", article_detail_api_view, name="article-detail"),
    path("articles/", ArticleListApiView.as_view(), name="article-list"),
    path("articles/<int:pk>", ArticleDetailApiView.as_view(), name="article-detail"),
    path("journalists/", JournalistListApiView.as_view(), name="journalist-list"),
    
]
