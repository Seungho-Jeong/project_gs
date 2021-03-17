from django.urls import path
from .views import GRNTInformation

urlpatterns = [
    path('/registration', GRNTInformation.as_view()),
    path('/registration/<int:model_information_id>', GRNTInformation.as_view()),
]