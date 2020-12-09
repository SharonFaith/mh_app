from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signupas, name='sign_up_as'),
    path('activate-account/<uid>/<token>/', views.activate_account, name='activation_email'),
]