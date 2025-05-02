from django.contrib import admin
from .models import Shift, Order, OrderMenu

class OrderMenuInline(admin.TabularInline):
    model = OrderMenu
    extra = 0
    fields = ('menu_product', 'quantity', 'price_part')
    readonly_fields = ('price_part',)
    autocomplete_fields = ('menu_product',)

class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    fields = ('id', 'customer', 'delivery_guy', 'state', 'price_total', 'order_date',)
    readonly_fields = ('id', 'customer', 'delivery_guy', 'state', 'price_total', 'order_date',)
    show_change_link = True

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('start', 'end', 'is_open', 'order_count')
    list_filter = ('start', 'end')
    ordering = ('-start',)
    readonly_fields = ('start',)
    search_fields = ('start',)
    inlines = [OrderInline]

    def is_open(self, obj):
        return obj.end is None
    is_open.boolean = True
    is_open.short_description = 'Open?'

    def order_count(self, obj):
        return obj.order_set.count()
    order_count.short_description = 'Total'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'shift', 'customer', 'delivery_guy', 'restaurant', 'state', 'price_total', 'order_date')
    list_filter = ('state', 'shift', 'delivery_guy', 'restaurant')
    search_fields = ('customer__name', 'customer__surname', 'delivery_guy__name', 'delivery_guy__surname')
    ordering = ('-order_date',)
    readonly_fields = ('order_date', 'delivery_date', 'price_total')
    autocomplete_fields = ('shift', 'delivery_guy', 'restaurant')
    inlines = [OrderMenuInline]

@admin.register(OrderMenu)
class OrderMenuAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_product', 'quantity', 'price_part')
    search_fields = ('menu_product__name',)
    autocomplete_fields = ('menu_product', 'order')