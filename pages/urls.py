from django.urls import path
from pages import views as v

urlpatterns = [
    path("", v.HomePageView.as_view(), name="home"),
]