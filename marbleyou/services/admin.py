from django.contrib import admin

from .models import WorkPrice, CalculationRequest, Feedback, Order


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'status', 'created_at')
    list_editable = ('status',)


class CalculationRequestAdmin(admin.ModelAdmin):
    list_display = ('product', 'id', 'name', 'email', 'status', 'created_at')
    list_editable = ('status',)
    search_fields = ['id']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'email', 'message', 'status', 'created_at')
    list_editable = ('status',)
    search_fields = ['id']


admin.site.register(CalculationRequest, CalculationRequestAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(WorkPrice)
