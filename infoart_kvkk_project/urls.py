"""
URL configuration for infoart_kvkk_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path
from django.conf import settings
import sportsint.views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from sportsint.views import KisiList

urlpatterns = [
#    path('admin/', admin.site.urls),
    path('contact/<uuid:pk>/', sportsint.views.contact, name='contact'),
    path('thank-you', sportsint.views.thank_you, name='thank-you'),
    path('talep_secim', sportsint.views.thank_you_nochoice, name='thank-you-nochoice'),
    path('failed', sportsint.views.failed, name='failed'),
    path("", sportsint.views.index, name="index"),
    path('consent/d3ee6b984fa6/', sportsint.views.getData),
    path('consent/lapis/', sportsint.views.getData),
    path('consent/sportsweb/', sportsint.views.getData),
    path('veriDonus/zder1848c2ac90b86/', sportsint.views.getDataResponse),
    path("api-token-auth/", obtain_auth_token, name='api-token-auth'),
    path('veriDonusPM/4aab8838-a108-4a85-9a7b-4a97f3d9f19a/', sportsint.views.getPostmanCsv),
    path('kayitlar/', KisiList.as_view(), name='kisi-list'),
]
