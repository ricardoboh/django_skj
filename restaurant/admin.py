from django.contrib import admin
from .models import Restaurant, MenuProduct

class MenuProductInline(admin.TabularInline):
    model = MenuProduct
    extra = 1
    fields = ('name', 'price')
    readonly_fields = ()

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')
    list_filter = ('name',)
    inlines = [MenuProductInline]

@admin.register(MenuProduct)
class MenuProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price')
    search_fields = ('name',)
    list_filter = ('restaurant',)
    ordering = ('restaurant', 'name')