from django.urls import path
from .views import *

urlpatterns = [
    path('', EventList.as_view(), name='index'),
    path('<int:pk>/', event_detail, name='event_detail'),
    # path('<int:pk>/', EventDetail.as_view(), name='event_detail'),
    path('<int:pk>/favorite_event/', favorite_event, name='favorite_event'),
    path('category/<int:pk>/', filter_by_category, name='category'),
    path('tag/<int:pk>/', filter_by_tag, name='tag'),
    path('date/', filter_by_date, name='date'),
    path('favorites/', event_favorite_list, name='event_favorite_list'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category-item/<int:pk>/', CategoryDetailView.as_view(), name="category_item"),
    path('<int:pk>/subscriber/', add_subscribes, name='add_subscribes'),
]