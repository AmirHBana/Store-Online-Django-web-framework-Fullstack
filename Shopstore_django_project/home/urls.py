from . import views
from django.urls import path, re_path

app_name = 'home'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    re_path(r'category/(?P<category_slug>[-\w]+)/', views.ProductListView.as_view(), name='category_filter'),
    re_path(r'reply/(?P<product_slug>[-\w]+)/(?P<comment_id>\d+)/', views.ProductAddReplyView.as_view(), name='add_reply'),
    re_path(r'v/(?P<slug>[-\w]+)/', views.ProductDetailView.as_view(), name='product_detail'),
]