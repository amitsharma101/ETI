from django.urls import path
from . import views

urlpatterns = [
    path('',views.auth),
    path('login_user',views.login_user,name='login_user'),
    path('auth',views.auth_response),
    path('profile',views.profile),
    path('edit_profile',views.edit_profile),
    path('logout_user',views.logout_user),
    path('verify_requests',views.verify_requests,name='verify_requests'),
]