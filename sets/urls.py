from django.urls import path
from .views import create_set,delete_set, create_card

app_name = "sets"

urlpatterns = [
    path('set_create/', create_set, name='set_create'),
    path('delete/<int:set_id>/', delete_set, name='delete'),
    path('create/<int:set_id>/', create_card, name='create'),
]