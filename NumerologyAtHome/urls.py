from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('home/', views.home),
    path('register/', views.register),
    path('login/', views.login),
    # User Urls
    path('userhome/', views.userhome),
    path('checkresult/', views.checkresult),
    path('askquery/', views.askquery),
    # Admin Urls
    path('adminhome/', views.adminhome),
    path('viewuser/', views.viewuser),
    path('manageuser/', views.manageuser),
    path('answerquery/', views.answerquery),
    # path('myadmin/', include('myadmin.urls')),
    # path('user/', include('user.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
