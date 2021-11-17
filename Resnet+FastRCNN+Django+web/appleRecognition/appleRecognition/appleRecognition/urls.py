"""appleRecognition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
import index.views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path(r'index/',index.views.index),
    path(r'about/', index.views.about),
    path(r'contact/', index.views.contact),
    path(r'projects/', index.views.projects),
    path(r'result/', index.views.result),
    path(r'show/', index.views.show),
    path(r'singlepost/', index.views.singlepost),
    path(r'suggest/', index.views.suggest),
    path(r'upload/', index.views.upload),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
