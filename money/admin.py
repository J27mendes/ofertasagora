from django.contrib import admin
from .models import Trend

@admin.register(Trend)
class TrendAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'interest', 'timestamp')
    search_fields = ('keyword',)