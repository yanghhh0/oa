"""oa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from oa import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'login/', views.login, name='login'),
    path(r'logout/', views.logout, name='logout'),
    path(r'register/', views.register, name='register'),
    path(r'teacher/', views.teacher, name='teacher'),
    path(r'data/', views.data, name='data'),
    path(r'check/', views.check, name='check'),
    path(r'manage/', views.manage, name='manage'),
    path(r'notice/', views.notice, name='notice'),
    path(r'qrcode/', views.make_qrcode, name='qrcode'),
    path(r'stuLogin/', views.stu_login, name='stuLogin'),
    path(r'stuIndex/', views.stu_index, name='stuIndex'),
    path(r'checkSetting/', views.check_setting, name='checkSetting'),
    path(r'checkHistory/', views.check_history, name='checkHistory'),
    path(r'getCheckTable/', views.get_record_table, name='getCheckTable')

]
