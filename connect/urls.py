from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', views.index, name ='index'),
    path('home/', views.home, name ='home'),
    path('register/',views.register,name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='django_registration/login.html'),name='login'),
    path('profile/<int:profile_id>/',views.profile,name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),

    path('inbox/', ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread/', CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name='create-message'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
