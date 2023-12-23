from django.urls import path

from . import views

app_name = 'favorites'

urlpatterns = [
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('clear/', views.FavoritesClearView.as_view(), name='favorites_clear'),
    path('<int:id>/add/', views.FavoritesCreateView.as_view(), name='add'),
]
