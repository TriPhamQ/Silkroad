from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^browse/(?P<category_name>[\w\-]+)/(?P<current_page>\d+)$', views.browse, name = 'browse'),
    url(r'^user$', views.user, name = 'user'),
    url(r'^product/(?P<product_id>\d+)$', views.product_page, name = 'product_page'),
    url(r'^add-to-cart/(?P<product_id>\d+)$', views.add_to_cart, name = 'add_to_cart')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
