from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<id>/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('addpost/', views.add_post, name='add_post'),
    path('rateworker/<profile_id>/', views.rate_worker, name='rate-worker'),
    path('reviewworker/<pro_id>/', views.add_review, name='review-worker'),
    path('prolist/', views.prolist, name='prolist'),
    path('userlist/', views.userlist, name='userlist'),
    path('activate-account/<uid>/<token>/', views.activate_account, name='activation_email'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 