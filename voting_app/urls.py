from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path
from polls import views

def create_admin(request):
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('emergencyadmin', 'emergency@example.com', 'EmergencyPass123!')
        return HttpResponse("Emergency admin created! Access at /admin/")
    return HttpResponse("Admin already exists")

urlpatterns = [
    path('create-admin-now/', create_admin),  # TEMPORARY - REMOVE AFTER USE
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('polls/', views.poll_list, name='poll_list'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('poll/<int:poll_id>/vote/', views.vote, name='vote'),
    path('poll/<int:poll_id>/results/', views.results, name='results'),
]


# urls.py (temporary)
from django.contrib.auth.models import User
from django.http import HttpResponse

def reset_all_passwords(request):
    for user in User.objects.all():
        user.set_password('temp_password_123')
        user.save()
    return HttpResponse("All passwords reset to 'temp_password_123'")