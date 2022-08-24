from django.urls import path
from django.urls.base import reverse_lazy
from .views import (
    deleteAccountView,
    editAccountView,
    registerView,
    loginView,
    logoutView,
)

app_name = 'account'

urlpatterns = [
    path('register', registerView, name='register'),
    path('login', loginView, name='login'),
    path('logout', logoutView, name='logout'),    
    path('edit_account/<int:accountId>',editAccountView, name='editAccount'),
    path('delete_account',deleteAccountView, name='deleteAccount'),
]