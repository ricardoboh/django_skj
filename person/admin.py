from django.contrib import admin
from .models import DeliveryGuy  # import DeliveryGuy

@admin.register(DeliveryGuy)
class DeliveryGuyAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone', 'hire_date', 'active')
    search_fields = ('name', 'surname', 'phone')
    list_filter = ('active', 'hire_date')
    ordering = ('-hire_date', 'surname')