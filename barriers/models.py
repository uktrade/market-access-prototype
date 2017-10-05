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


class BarrierRecord(AuditableModel):
    """
    An HMG record of a barrier - created automatically from an entry
    in the EC or WTO database, because a case worker created a record
    based on a report, or because a case worker created a record from
    scratch based on some other information.
    """
    BARRIER_RECORD_STATUS_ACTIVE = "Active"
    # more statuses to be added soon...
    BARRIER_RECORD_STATUS_CHOICES = (
        (BARRIER_RECORD_STATUS_ACTIVE, "Active"),
    )
    status = models.CharField(
        max_length=10,
        choices=BARRIER_RECORD_STATUS_CHOICES,
        default=None,
        null=True, blank=True
    )
    title = models.TextField(
        _('Title'),
        blank=True
    )
    description = models.TextField(
        _('Description'),
        blank=True
    )
    # TODO: convert products to a table lookup
    products_text = models.TextField(
        _('Products affected'),
        blank=True
    )
    # TODO: convert sectors to a table lookup
    sectors_text = models.TextField(
        _('Sectors affected'),
        blank=True
    )
    country = models.ForeignKey(
        'BarrierCountry',
        null=True, blank=True
    )
    barrier_source = models.ForeignKey(
        'BarrierSource'
    )
    source_id = models.CharField(
        _('ID in source system'),
        max_length=20,
        null=True, blank=True
    )
    barrier_types = TreeManyToManyField(
        'BarrierType',
        blank=True,
        related_name='types',
        db_index=True
    )
    distribution_date = models.DateField(
        _('Distribution Date'),
        null=True, blank=True
    )
    external_link = models.CharField(
        _('External site link'),
        max_length=1500, blank=True
    )

class BarrierNotification(AuditableModel):
    """
    Information about a barrier that has come
    from the EC MADB or WTO databases.
    """

    title = models.TextField(
        _('Title'),
        blank=True
    )
    description = models.TextField(
        _('Description'),
        blank=True
    )
    distribution_date = models.DateField(
        _('Distribution Date'),
        null=True, blank=True
    )
    # where did this barrier information come from?
    barrier_source = models.ForeignKey(
        'BarrierSource'
    )
    # remember Django gives us an 'id' primary key by default, we don't have to define one
    # some WTO entries from CSV file have multiple symbols concatenated,
    # right now we ignore and just take the first one
    barrier_symbol = models.CharField(
        _('Barrier Symbol'),
        max_length=500,
        blank=True
    )
    # this ignores parts like "/Add.1" at the end so we can group notifications together
    core_symbol = models.CharField(
        _('Core Symbol'),
        max_length=500, blank=True
    )
    # extracted from the WTO symbol, this is always "SPS" or "TBT" for now
    mab_type = models.CharField(_('Barrier type'), max_length=500, blank=True)
    country = models.ForeignKey(
        'BarrierCountry',
        related_name='notification_countries',
        null=True, blank=True
    )
    products_text = models.TextField(_('Products'), blank=True)
    product_codes = models.TextField(_('Product codes'), blank=True)
    objectives = models.TextField(_('Objectives'), blank=True)
    # SPS only
    keywords = models.TextField(_('Keywords'), blank=True)
    # SPS only
    regions_affected = models.TextField(
        _('Regions affected'),
        blank=True
    )
    comments_due_date = models.DateField(
        _('Final date for comments'),
        null=True, blank=True
    )
    notification_type = models.CharField(
        _('Notification type'),
        max_length=50,
        blank=True
    )
    document_link = models.CharField(
        _('Document link'),
        max_length=1500,
        blank=True
    )
    external_link = models.CharField(
        _('External site link'),
        max_length=1500, blank=True
    )
    # Categorisation of barriers
    # barrier_type = TreeForeignKey('BarrierType', null=True, blank=True, related_name='barrier_type', db_index=True)
    barrier_types = TreeManyToManyField(
        'BarrierType',
        blank=True,
        related_name='barrier_types',
        db_index=True
    )
    
    def __str__(self):
        return self.title

    @staticmethod
    def get_countries():
        from django.db.models import Count
        return get_user_model().objects.values("notifying_member").annotate(count=Count("id")).order_by('-count')


class BarrierReporter(AuditableModel):
    """
    Person who has filled in a barrier report.
    """
    name = models.CharField(_('Reporter name'), max_length=1500, blank=True)
    company = models.CharField(_('Company name'), max_length=1500, blank=True)


class BarrierReport(AuditableModel):
    """
    A report from a member of the public (or from someone at a post)
    """

    BARRIER_REPORT_STATUS_DRAFT = "Draft"
    BARRIER_REPORT_STATUS_SUBMITTED = "Submitted"
    BARRIER_REPORT_STATUS_CHOICES = (
        (BARRIER_REPORT_STATUS_DRAFT, "Draft"),
        (BARRIER_REPORT_STATUS_SUBMITTED, "Submitted"),
    )
    status = models.CharField(
        max_length=10,
        choices=BARRIER_REPORT_STATUS_CHOICES,
        default=None,
        null=True, blank=True
    )
    reporter = models.ForeignKey(
        'BarrierReporter',
        null=True, blank=True
    )
    # name won't be filled in straight away
    name = models.CharField(
        max_length=200,
        null=True, blank=True
    )
    problem_description = models.TextField(
        null=True, blank=True
    )
    product_text = models.TextField(
        null=True, blank=True
    )
    product_code = models.CharField(
        max_length=500,
        null=True, blank=True
    )
    country = models.ForeignKey(
        'BarrierCountry',
        null=True, blank=True
    )
    #export_to_other_countries_flag = models.NullBooleanField(
    #    _('Do you export this product/service to other countries?'),
    #    null=True, blank=True
    #)
    #other_countries_problem_description = models.TextField(
    #    null=True, blank=True
    #)
    business_impact_description = models.TextField(
        null=True, blank=True
    )
    problem_duration_description = models.TextField(
        null=True, blank=True
    )
    OTHER_COMPANIES_AFFECTED_YES = "Yes"
    OTHER_COMPANIES_AFFECTED_NO = "No"
    OTHER_COMPANIES_AFFECTED_DONTKNOW = "DontKnow"
    OTHER_COMPANIES_AFFECTED_CHOICES = (
        (OTHER_COMPANIES_AFFECTED_YES, "Yes"),
        (OTHER_COMPANIES_AFFECTED_NO, "No"),
        (OTHER_COMPANIES_AFFECTED_DONTKNOW, "Don't know")
    )
    other_companies_affected_choice = models.CharField(
        max_length=10,
        choices=OTHER_COMPANIES_AFFECTED_CHOICES,
        default=None,
        null=True, blank=True
    )
    other_countries_affected_description = models.TextField(
        null=True, blank=True
    )
    top_level_barrier_type = models.ForeignKey(
        'BarrierType',
        related_name='barrier_reports',
        null=True, blank=True
    )
    steps_taken_to_resolve = models.TextField(
        null=True, blank=True
    )
    outcome_looking_for = models.TextField(
        null=True, blank=True
    )
    SUPPORT_DESIRED_NONE = 'None'
    SUPPORT_DESIRED_LOCAL = 'Local'
    SUPPORT_DESIRED_BROAD = 'Broad'
    SUPPORT_DESIRED_NOT_SURE = 'Broad'
    SUPPORT_DESIRED_CHOICES = (
        ('SUPPORT_DESIRED_NONE', 'None - this is for your information only'),
        ('SUPPORT_DESIRED_LOCAL', 'Local engagement only with UK Government officials in the country I am trying to export to'),
        ('SUPPORT_DESIRED_BROAD', 'Broader UK Government involvement'),
        ('SUPPORT_DESIRED_NOT_SURE', 'Not sure'),
    )
    support_desired_choice = models.CharField(
        max_length=10,
        choices=SUPPORT_DESIRED_CHOICES,
        default=None,
        null=True, blank=True
    )
    confidentiality_issues_description = models.TextField(
        null=True, blank=True
    )
    HAPPY_TO_PUBLISH_YES = 'Yes'
    HAPPY_TO_PUBLISH_NO = 'No'
    HAPPY_TO_PUBLISH_MAYBE = 'Maybe'
    HAPPY_TO_PUBLISH_CHOICES = (
        ('HAPPY_TO_PUBLISH_YES', 'Yes'),
        ('HAPPY_TO_PUBLISH_NO', 'No'),
        ('HAPPY_TO_PUBLISH_MAYBE', 'Maybe, following consultation with me'),
    )
    happy_to_publish_choice = models.CharField(
        max_length=10,
        choices=HAPPY_TO_PUBLISH_CHOICES,
        default=None,
        null=True, blank=True
    )
    any_other_details_description = models.TextField(
        null=True, blank=True
    )


class BarrierSource(AuditableModel):
    """
    Source of barrier info - either UK, WTO or EC MADB
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True, blank=True)
    short_name = models.CharField(max_length=20, null=True, blank=True)
    remote_url = models.URLField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.short_name


class BarrierType(MPTTModel, AuditableModel):
    """
    Barrier types are hierarchical - implementation provided by MPTTModel

    We provide a different set of barrier types for each source (HMG, WTO, EC, UNCTAD)
    so that we can re-purpose the original source information and map between them
    """
    barrier_source = models.ForeignKey(
        'BarrierSource',
        default=1 # default to UK as a barrier source
    )
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, null=True, blank=True)
    barrier_code = models.CharField(max_length=20, null=True, blank=True)
    is_sps = models.BooleanField(default=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        # return str(self.barrier_source) + ':' + str(self.name)
        return str(self.name)

    def multiselect_label(self, obj):
        return obj.barrier_code + ': ' + obj.name

class BarrierTypeMapping(AuditableModel):
    """
    Mapping between one of the existing barrier type lists and ours.
    """
    source_barrier_list = models.ForeignKey(
        'BarrierSource',
        related_name = 'source_barrier_list'
    )
    source_barrier_type = models.ForeignKey(
        'BarrierType',
        related_name = 'source_barrier_type'
    )
    destination_barrier_list = models.ForeignKey(
        'BarrierSource',
        related_name = 'destination_barrier_list'
    )
    destination_barrier_type = models.ForeignKey(
        'BarrierType',
        related_name = 'destination_barrier_type'
    )
    def __str__(self):
        return str(self.source_barrier_type)+' to '+str(self.destination_barrier_type)

class BarrierCountry(AuditableModel):
    """
    Country or Territory - values taken from the GOV.UK register
    https://country.register.gov.uk/records
    https://territory.register.gov.uk/records
    Note: Should establish a procedure for updating these periodically
    """
    name = models.CharField(
        _('Country or Territory Name'),
        max_length=100
    )
    code = models.CharField(
        _('Country or Territory Code'),
        max_length=100,
        null=True,
        blank=True
    )
    official_name = models.CharField(
        _('Offical Country or Territory name'),
        max_length=100,
        null=True, blank=True
    )
    govuk_index_entry_code = models.CharField(
        _('GOV.UK index code'),
        max_length=20,
        null=True, blank=True
    )
    # used in the below field
    COUNTRY_TYPE_COUNTRY = 'country'
    COUNTRY_TYPE_TERRITORY = 'territory'
    COUNTRY_TYPE_BLOC = 'bloc'
    COUNTRY_TYPE_CHOICES = (
        (COUNTRY_TYPE_COUNTRY, 'Country'),
        (COUNTRY_TYPE_TERRITORY, 'Territory'),
        (COUNTRY_TYPE_BLOC, 'Trade Bloc'),
    )
    country_or_territory = models.CharField(
        _('Country or Territory flag'),
        max_length=10, choices=COUNTRY_TYPE_CHOICES, default=COUNTRY_TYPE_COUNTRY
    )

    def __str__(self):
        return self.name

    def get_type(self):
        return self.get_country_or_territory_display()

    get_type.short_description = 'Type'

    class Meta:
        verbose_name_plural = 'countries or territories'
