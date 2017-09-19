# marketaccess/admin.py

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter
from .models import MarketAccessBarrier, BarrierType


class MarketAccessBarrierAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    date_hierarchy = 'distribution_date'
    # fields to display on list page
    list_display = ('pk', 'core_symbol', 'wto_symbol', 'title', 'notifying_member', 'notification_type', 'distribution_date')
    # fields to filter by on list page
    list_filter = (
        ('barrier_types', TreeRelatedFieldListFilter),
        'notification_type', 'notifying_member', 
    )
    # enables search in the admin
    search_fields = ['core_symbol', 'wto_symbol', 'title', 'notifying_member', 'notification_type', ]


# class BarrierTypeAdmin(MPTTModelAdmin):
class BarrierTypeAdmin(DraggableMPTTAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'is_sps', 'ec_barrier_code')


admin.site.register(MarketAccessBarrier, MarketAccessBarrierAdmin)
admin.site.register(BarrierType, BarrierTypeAdmin)
