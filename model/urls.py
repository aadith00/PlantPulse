from django.urls import path
from .views import modpage

urlpatterns = [
    path('diseaseprediction', modpage, name='model'),
]
