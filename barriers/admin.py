# marketaccess/admin.py

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter
from .models import (
    BarrierRecord, BarrierNotification,
    BarrierReport,
    # lookup tables
    BarrierType, BarrierSource, BarrierCountry, BarrierTypeMapping
)


class BarrierRecordAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    date_hierarchy = 'distribution_date'
    # fields to display on list page
    list_display = (
        'pk', 'barrier_source', 'source_id',
        'title', 'country', 'distribution_date'
    )
    # fields to filter by on list page
    list_filter = (
        'barrier_source',
        ('barrier_types', TreeRelatedFieldListFilter),
        'country', 
    )
    # enables search in the admin
    search_fields = [
        'core_symbol', 'barrier_symbol', 'title',
        'country', 'notification_type', 
    ]


class BarrierNotificationAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'barrier_source', 'barrier_symbol',
        'title', 'country', 'distribution_date'
    )
    pass


class BarrierReportAdmin(admin.ModelAdmin):
    pass


class BarrierTypeMappingInline(admin.TabularInline):
    """BarrierTypeMapping is edited inside BarrierType"""
    model = BarrierTypeMapping
    extra = 0
    fk_name = 'source_barrier_type'


class BarrierTypeAdmin(DraggableMPTTAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    list_display = (
        'tree_actions',
        'barrier_source',
        'indented_title',
        'barrier_code',
        # 'description',
        'is_sps'
    )
    list_filter = (
        'barrier_source',
    )
    search_fields = [
        'name',
        'description'
    ]
    inlines = [ BarrierTypeMappingInline ]


class BarrierSourceAdmin(admin.ModelAdmin):
    pass


class BarrierCountryAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'code', 'get_type' )

class BarrierTypeMappingAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'source_barrier_list',
        'source_barrier_type',
        'destination_barrier_list',
        'destination_barrier_type'
    )

admin.site.register(BarrierRecord, BarrierRecordAdmin)
admin.site.register(BarrierNotification, BarrierNotificationAdmin)
admin.site.register(BarrierReport, BarrierReportAdmin)
admin.site.register(BarrierType, BarrierTypeAdmin)
admin.site.register(BarrierSource, BarrierSourceAdmin)
admin.site.register(BarrierCountry, BarrierCountryAdmin)
admin.site.register(BarrierTypeMapping, BarrierTypeMappingAdmin)

