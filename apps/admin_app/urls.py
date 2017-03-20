from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin$', views.admin, name = 'admin'),
    url(r'^signout$', views.signout, name = 'signout'),
    url(r'^products$', views.products, name = 'products'),
    url(r'^orders$', views.orders, name = 'orders'),
    url(r'^add_product$', views.add_product, name = 'add_product'),
    url(r'^stop_sale_product/(?P<product_id>\d+)$', views.stop_sale_product, name = 'stop_sale_product'),
    url(r'^restart_sale_product/(?P<product_id>\d+)$', views.restart_sale_product, name = 'restart_sale_product'),
    url(r'^edit_product/(?P<product_id>\d+)$', views.edit_product, name = 'edit_product'),
    url(r'^submit_edited_product/(?P<product_id>\d+)$', views.submit_edited_product, name = 'submit_edited_product'),
    url(r'^order-status-update$', views.order_status_update, name = 'order_status_update'),
    url(r'^clear_db$', views.clear_db, name = 'clear_db')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
