from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField 
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
       name = models.CharField(max_length=150, unique=True)
       parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
       slug = models.SlugField(max_length=150, unique=True, allow_unicode=True)
       created_at = models.DateTimeField(auto_now_add=True)

       
       class MPTTMeta:
           order_insertion_by = ['name']

       def __str__(self):
           return self.name
       
       def get_absolute_url(self):
            return reverse('home:category_filter', args=[self.slug,])
		  
		    

class Product(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', default='')
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200)
    image = ResizedImageField(scale=0.7 ,size=[220 , 220],quality=85, crop=['middle', 'center'], upload_to='')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    
    description = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:product_detail', args=[self.slug,])
    
 

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pcomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user} - {self.body[:30]}'


   
