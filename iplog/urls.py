"""iplog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from logger import views
from django.contrib.auth.views import LogoutView
import iplog.settings as settings


urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("view_res/<admin_url>", views.admin_url_view, name='view_res'),
    path("catch/<victim_url>", views.catch_ip),
    path("create_logger/<type_>/<asset>", views.create_logger_view, name='create_logger'),
    path("delete_logger/<id_>", views.delete_logger, name='delete_logger'),
    path("profile", views.profile_view),
    path("login", views.login_view, name="login"),
    path("logout", LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name="logout")
]
