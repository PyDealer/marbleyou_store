from django.contrib import admin

from .models import (
    Product, Stone, Category, Genus, ProductAlbum,
    StoneAlbum, HomePage, HomePageAlbum
)


class HomePageImageInline(admin.StackedInline):
    model = HomePageAlbum
    extra = 3


class HomePageAdmin(admin.ModelAdmin):
    inlines = [HomePageImageInline, ]


class StoneImageInline(admin.StackedInline):
    model = StoneAlbum
    extra = 3


class StoneAdmin(admin.ModelAdmin):
    inlines = [StoneImageInline, ]
    list_display = ('name', 'price', 'is_published')
    list_editable = ('is_published',)


class ProductImageInline(admin.StackedInline):
    model = ProductAlbum
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]
    list_display = ('title', 'is_published')
    list_editable = ('is_published',)


class GenusAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stone, StoneAdmin)
admin.site.register(Genus, GenusAdmin)
admin.site.register(HomePage, HomePageAdmin)
