from django.urls import path
from .views import model_page,model_prediction_view


urlpatterns = [
    path('diseaseprediction', model_page, name='model'),
    path('model/',model_prediction_view, name='model_prediction'),
]