from django.urls import path
from .views import search_view, reindex_view

urlpatterns = [
    path('', search_view, name='search'),
    path('reindex/', reindex_view, name='reindex'),  # triggers (re)index of sample docs
]