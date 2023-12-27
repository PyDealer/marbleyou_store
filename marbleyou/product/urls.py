from django.urls import path

from . import views

app_name = 'product'

urlpatterns = [
     path('', views.CategoryListView.as_view(), name='index'),
     path('product/<slug:category_slug>/',
          views.CategoryDetailView.as_view(),
          name='products'),
     path('product/<slug:category_slug>/<slug:detail_prod_slug>/',
          views.ProductDetailView.as_view(),
          name='product_detail'),
     path('<slug:stone_slug>/',
          views.StoneDetailView.as_view(),
          name='stone_detail'),
     path('result/', views.ResultTemplateView.as_view(),
          name='result'),
     path('question/', views.QuestionFormView.as_view(),
          name='question'),
     path('calculator/', views.CalculatorFormView.as_view(),
          name='calculator'),
]
