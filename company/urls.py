from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "company"

urlpatterns = [
    path("list", views.CompanyListView.as_view(), name="list"),
    path("create", views.CompanyCreateView.as_view(), name="create"),
    path("<kurulus_id>", views.CompanyCRUDView.as_view(), name="crud"),
]
