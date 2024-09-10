from django.urls import path
from .views import modpage,model_prediction_view


urlpatterns = [
    path('diseaseprediction', modpage, name='model'),
    path('model/',model_prediction_view, name='model1'),
]




