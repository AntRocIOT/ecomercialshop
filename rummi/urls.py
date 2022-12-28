"""rummi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from tenda.views import RegisterUserView,LoginView,LogoutView
from tenda import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', views.buscar, name='buscar'),
    url(r'^filtra',views.filtra,name='filtra'),
    url(r'^search_category', views.search_category, name='search_category'),
    url(r'^create_product', views.create_product, name='create_product'),
    url(r'^product_list/$', views.product_list, name='product_list2'),
    url(r'^product_list/(?P<product_id>\d+)/edit/$', views.edit_product, name='edit_product2'),
    url(r'^product_list/(?P<product_id>\d+)/eliminate/$', views.delete_product, name='eliminate_product2'),
    
	#Payment
    url(r'^payment$', views.payment, name='payment'),
    url(r'^payment_last$', views.payment, name='payment_last'),

    url(r'^payment/success$', views.success_payment, name='success_payment'),
    url(r'^payment/canceled$', views.unsuccess_payment, name='unsuccess_payment'),

    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^tickets$',views.tickets_list,name='tickets_list'),
    
    
    url(r'^product/(?P<id_product>\d+)',views.product, name='product'),
    url(r'^profile', views.profile_edit, name='profile'),
    #Cart
    url(r'^cart$', views.cart_list, name='cart'),
    url(r'^cart/add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^cart/remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
    
    #Admin zone
    url(r'^admin/$', views.admin_zone, name='admin_zone'),
    url(r'^admin/user_list/$', views.admin_zone_user_list, name='admin_zone_user_list'),
    url(r'^admin/user_list/(?P<user_id>\d+)/edit/$', views.admin_zone_edit_user, name='edit_users'),
    url(r'^admin/user_list/(?P<user_id>\d+)/eliminate/$', views.admin_zone_eliminate_user, name='eliminate_users'),
    url(r'^admin/user_list/create/$', views.admin_zone_create_users, name='create_users'),
    url(r'^admin/product_list/$', views.admin_zone_product_list, name='product_list'),
    url(r'^admin/product_list/(?P<product_id>\d+)/edit/$', views.admin_zone_edit_product, name='edit_product'),
    url(r'^admin/product_list/(?P<product_id>\d+)/eliminate/$', views.admin_zone_eliminate_product, name='eliminate_product'),
    url(r'^admin/product_list/create/$', views.admin_zone_create_product, name='admin_create_product'),
    url(r'^admin/payments_list/$', views.admin_zone_payments_list, name='payments_list'),

    url(r'^login', view=LoginView.as_view(),name='login'),
    url(r'^logout', views.logout_session, name='logout'),
    url(r'^registre', view=RegisterUserView.as_view(), name='registre'),
    url(r'^resultats_consulta', views.resultats_consulta, name='resultats_consulta.html'),
    url(r'^anunci', views.anunci, name='anunci.html'),
    url(r'^ajuda', views.ajuda, name='ajuda.html'),
    



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
