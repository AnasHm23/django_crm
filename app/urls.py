# urls.py

from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomPasswordResetView, CustomPasswordResetConfirmView

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('record/<int:id>/', views.record, name='record'),
    path('delete_record/<int:id>/', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:id>/', views.update_record, name='update_record'),
    path('youtube/', views.youtube, name='youtube'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.home, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('api/', include('app.api_urls')),
]
