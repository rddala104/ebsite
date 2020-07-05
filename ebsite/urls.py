# -*- coding: utf-8 -*-

from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf.urls import url, re_path
from django.conf import settings

urlpatterns = [
    re_path(r'^bienvenue$', views.bienvenito, name='bienvenue'),
    re_path(r'^sign-in/(?P<goto>\w+:\w+)/$',views.sign_in, name='sign_in_goto'),
    re_path(r'^sign-in/$', views.sign_in, name='sign_in'),
    re_path(r'^sign-out/$', views.sign_out, name='sign_out'),
    re_path(r'^boutique/$', views.boutique, name='boutique'),
    re_path(r'^article/(?P<id>\d+)/$', views.detail, name='detail'),
    re_path(r'^add-to-cart/(?P<product_id>\d+)/(?P<qty>\d+)/$', views.add_to_cart, name='add_to_cart'),
    re_path(r'^clear-cart/$', views.clear_cart, name='clear_cart'),
    re_path(r'^cart/$', views.display_cart, name='display_cart'),
    re_path(r'^shipping/$', views.shipping, name='shipping'),
    re_path(r'^add-address/$', views.add_address, name='add_address'),
    re_path(r'^checkout/$', views.checkout, name='checkout'),
    re_path(r'^confirmation/$', views.confirmation, name='confirmation'),
    re_path(r'^account/$', views.account, name='account'),
    re_path(r'^orders/$', views.orders, name='orders'),
    re_path(r'^addresses/$', views.addresses, name='addresses'),
    re_path(r'^authentification/$', views.authentification, name='authentification'),
    re_path(r'^muraidee/$', views.envoimess, name='muraidee'),
    re_path(r'^envoimess/$', views.envoimess, name='envoimess'),
       ] 
    #    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)