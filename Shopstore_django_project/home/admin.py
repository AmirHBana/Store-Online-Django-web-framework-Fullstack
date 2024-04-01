from __future__ import absolute_import
from django.contrib import admin
from .models import Category, Product, Comment



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "updated", "created")
	raw_id_fields = ('category',)
	prepopulated_fields = {'slug':('name',)}
    
	

@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
	list_display = ( "name",)
	prepopulated_fields = {'slug':('name',)}


	
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created', 'is_reply')
    raw_id_fields = ('user', 'product', 'reply')
    
