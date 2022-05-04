from django.contrib import admin
from .models import Brand, Category

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


