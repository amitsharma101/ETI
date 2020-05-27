from django.urls import path
from . import views

urlpatterns = [
    path('',views.auth),
    path('auth',views.auth_response),
]