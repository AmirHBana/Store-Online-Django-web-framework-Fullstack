from django.contrib.sitemaps import Sitemap
from .models import Product, Comment,Category
class ProductSitemap(Sitemap):
    changefreq = "never"
    priority = 0.7

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated
    

