from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
     path("profile/", profile, name="profile"),
    path('login/', login_user,name='login'),
    path('signup-u/', signup_user, name="signup"),  
    path('signup-b/', signup_business, name="signup-b"),  
    path('logout/', logout_u, name="logout"),  
    path('add-products/', add_products, name="add-products"),
    path('activate/<uuid:token>/', verify, name="verify_users"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="authentication/password-reset.html", title="PASSWORD"), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="authentication/password-reset-done.html", title="PASSWORD"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="authentication/password-reset-confirm.html", title="PASSWORD"), name="password_reset_confirm"),
    path("password-reset-confirm/MQ/set-password/", auth_views.PasswordResetCompleteView.as_view(template_name="authentication/password-reset-complete.html", title="PASSWORD"), name="password_reset_complete"),
]
