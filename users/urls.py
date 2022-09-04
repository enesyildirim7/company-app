from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login", views.UserLoginView.as_view(), name="login"),
    path("signup", views.UserSignupView.as_view(), name="signup"),
    path("logout", views.UserLogoutView.as_view(), name="logout"),
    path("me", views.UserDataView.as_view(), name="me"),
    path("follow", views.CompanyFollowView.as_view(), name="follow"),
]