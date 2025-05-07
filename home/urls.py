'''
URL paths for home app
'''

from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home")
]