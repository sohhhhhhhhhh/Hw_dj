from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('data/', views.get_data, name='get_data'),
    path('info/', views.get_info, name='get_info'),
    path('post/', views.post_data, name='post_data'),
    path('combined/', views.combined, name='combined'),
    path('register/', views.register, name='register'),
    path('login1/', views.login_user, name='login'),

    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),

]




