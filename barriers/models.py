# marketaccess/models.py

import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField

class AuditableModel(models.Model):
    """
    Shared model giving audit-trail capabilities to any child class.
    """
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        # don't create two tables, just add the above fields to any child object's table
        abstract = True

class MarketAccessBarrier(AuditableModel):
    """
    MarketAccessBarrier
    Inspired by ePing notification service from the WTO.
    To be expanded to locally initiated barriers as well.

    Design note: we could use OO to make an SPSBarrier, TBT etc
    But I think the types are too fluid right now
    So let's just have one object for everything and a 'type' field
    """

    # remember Django gives us an 'id' primary key by default, we don't have to define one
    # some WTO entries from CSV file have multiple symbols concatenated,
    # right now we ignore and just take the first one
    wto_symbol = models.CharField(_('WTO Symbol'), max_length=500, blank=True)
    # this ignores parts like "/Add.1" at the end so we can group notifications together
    core_symbol = models.CharField(_('Core Symbol'), max_length=500, blank=True)
    # extracted from the WTO symbol, this is always "SPS" or "TBT" for now
    mab_type = models.CharField(_('Barrier type'), max_length=500, blank=True)
    # turn this into a country lookup code?? make it one:many?
    notifying_member = models.CharField(_('Notifying Member(s)'), max_length=100, blank=True)
    title = models.TextField(_('Title'), blank=True)
    description = models.TextField(_('Description'), blank=True)
    distribution_date = models.DateField(_('Distribution Date'), null=True, blank=True)
    products_text = models.TextField(_('Products'), blank=True)
    product_codes = models.TextField(_('Product codes'), blank=True)
    objectives = models.TextField(_('Objectives'), blank=True)
    # SPS only
    keywords = models.TextField(_('Keywords'), blank=True)
    # SPS only
    regions_affected = models.TextField(_('Regions affected'), blank=True)
    comments_due_date = models.DateField(_('Final date for comments'), null=True, blank=True)
    notification_type = models.CharField(_('Notification type'), max_length=50, blank=True)
    document_link = models.CharField(_('Document link'), max_length=1500, blank=True)
    wto_link = models.CharField(_('WTO ePing link'), max_length=1500, blank=True)
    # Categorisation of barriers
    # barrier_type = TreeForeignKey('BarrierType', null=True, blank=True, related_name='barrier_type', db_index=True)
    barrier_types = TreeManyToManyField('BarrierType', blank=True, related_name='barrier_types', db_index=True)
    
    def __str__(self):
        return self.title

    @staticmethod
    def get_countries():
        from django.db.models import Count
        return get_user_model().objects.values("notifying_member").annotate(count=Count("id")).order_by('-count')

class BarrierType(MPTTModel, AuditableModel):
    """
    Barrier types are hierarchical - implementation provided by MPTTModel
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True, blank=True)
    ec_barrier_code = models.CharField(max_length=20, blank=True, null=True)
    is_sps = models.BooleanField(default=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
