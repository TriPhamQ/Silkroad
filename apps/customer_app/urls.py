from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^browse/(?P<category_name>[\w\-]+)/(?P<current_page>\d+)$', views.browse, name = 'browse'),
    url(r'^user$', views.user, name = 'user'),
    url(r'^shopping-cart$', views.shopping_cart, name = 'shopping_cart'),
    url(r'^check-out$', views.check_out, name = 'check_out'),
    url(r'^product/(?P<product_id>\d+)$', views.product_page, name = 'product_page'),
    url(r'^add-to-cart/(?P<product_id>\d+)$', views.add_to_cart, name = 'add_to_cart'),
    url(r'^change-quantity/(?P<product_id>\d+)$', views.change_quantity, name = 'change_quantity'),
    url(r'^remove-item/(?P<product_id>\d+)$', views.remove_cart_item, name = 'remove_cart_item'),
    url(r'^place-order$', views.place_order, name = 'place_order'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
