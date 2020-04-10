from django.contrib import admin
from .models import LeadModel

@admin.register(LeadModel)
class LeadAdminModel(admin.ModelAdmin):
    list_display = ('__str__','referrer', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('referrer', )

# admin.site.register(LeadModel)