from django.contrib import admin
from django.urls import path
from polls import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('polls/', views.poll_list, name='poll_list'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('poll/<int:poll_id>/vote/', views.vote, name='vote'),
    path('poll/<int:poll_id>/results/', views.results, name='results'),
]