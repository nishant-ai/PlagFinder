from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name="home-page"),
    path('plag-test/', dev_page, name="plag-test"),
    # path('dev/', dev_page)
]
