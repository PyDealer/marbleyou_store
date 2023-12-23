from django.urls import path

from .views import ContactsView

app_name = 'about'

urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
]
