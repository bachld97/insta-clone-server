from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.register),
    path('login/', views.token),
    path('autologin/', views.refresh_token),
    path('logout/', views.revoke_token),
]
