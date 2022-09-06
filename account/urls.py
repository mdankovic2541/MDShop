from django.urls import path
from django.urls.base import reverse_lazy
from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from .views import (
    deleteAccountView,
    editAccountView,
    registerView,
    loginView,
    logoutView,
    profileView,
    analyticsView,
)
from .forms import UserPasswordResetForm

app_name = 'account'

urlpatterns = [
    path('register', registerView, name='register'),
    path('login', loginView, name='login'),
    path('logout', logoutView, name='logout'), 
    path('profile', profileView, name='profile'),  
    path('analytics', analyticsView, name='analytics'),   
    path('edit_account/<int:accountId>',editAccountView, name='editAccount'),
    path('delete_account',deleteAccountView, name='deleteAccount'),
    # ! Reset and Change Password
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('password_change/', PasswordChangeView.as_view(template_name='registration/password_change.html', success_url=reverse_lazy('account:password_change_done')), name='password_change'),
    path('password_reset/done/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),    
    path('reset/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(success_url= reverse_lazy('account:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('password_reset/', PasswordResetView.as_view(success_url = reverse_lazy('account:password_reset_done'), template_name='registration/password_reset_form.html', form_class=UserPasswordResetForm),name='password_reset'),
]