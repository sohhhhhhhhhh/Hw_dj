from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.home, name='home'),
    path('data/', views.get_data, name='get_data'),
    path('info/', views.get_info, name='get_info'),
    path('post/', views.post_data, name='post_data'),
    path('combined/', views.combined, name='combined'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('restore-account/<str:token>/<str:email>/', views.restore_account, name='restore_account'),

    path('profile/', views.profile, name='profile'),

    path('logout/', views.logout_user, name='logout_user'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

