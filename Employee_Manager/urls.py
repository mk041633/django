from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('dashboard/', include('Employee_Dashboard.urls')),
    path('Dashboard/', include('Employer_Dashboard.urls')),
    path('', views.DefaultView, name='ndefault'),
]