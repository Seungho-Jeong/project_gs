from django.urls import path
from .views import SignUpView, SignInView, SignInKakaoView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/signin/kakao', SignInKakaoView.as_view()),
]