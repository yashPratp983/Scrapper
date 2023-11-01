from django.urls import path,include
from .views import Navigate

urlpatterns = [
    path('Navigate/', Navigate,name='Navigate'),
]