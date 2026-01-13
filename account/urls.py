from django.urls import path, include
from .views import register, dashboard, edit
from learn_sessions.views import results

# app_name = 'account'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('results/', results, name='results')
]