from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from . import views



 
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('upload/', views.upload,name='upload'),
    path('login/', views.loginPage,name='login'),
    path('logout/', views.logoutUser,name='logout'),
    path('register/', views.register,name='register'),
    path('check/', views.check,name='check'),


    url('associateCourse', views.associateCourse, name='associateCourse'),
    url('checkCourse', views.checkCourse, name='checkCourse'), 
    url('chart', views.chart, name='chart'),
    url('cpredict', views.cpredict, name='cpredict'),
    url('cpredictCourse', views.cpredictCourse, name='cpredictCourse'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


