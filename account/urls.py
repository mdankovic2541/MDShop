from django.urls import path
from django.urls.base import reverse_lazy
from .views import (
    registerView,
    loginView,
    logoutView,
)

app_name = 'account'

urlpatterns = [
    path('register', registerView, name='register'),
    path('login', loginView, name='login'),
    path('logout', logoutView, name='logout'),    
]