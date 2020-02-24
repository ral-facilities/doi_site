"""doi_site URL Configuration

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
from django.urls import path
from doi_site.views import HomeView, DoiList, Domains, Notes, Login_view
from django.conf.urls import include, url

from datasets.views import Mint

urlpatterns = [
    path(r'', HomeView.as_view(), name='home'),
    path(r'index', HomeView.as_view(), name='index'),

    #path(r'^admin/', include(admin.site.urls)),

    path(r'doilist', DoiList.as_view(), name='doi_list'),
    path(r'domains', Domains.as_view(), name='domains'),
    path(r'mint', Mint.as_view(), name='mint'),
    path(r'notes', Notes.as_view(), name='notes'),

    path(r'accounts/login/', Login_view.as_view(), name="login"),


    path(r'', HomeView.as_view())
]
