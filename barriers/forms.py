# barriers/forms.py

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import BarrierReport, BarrierReporterOrganisation

class BarrierCountryForm(forms.Form):
    countries_affected = forms.CharField(label='Country affected', max_length=100)

    # BarrierReport fields
    #status = models.CharField( max_length=10, choices=BARRIER_REPORT_STATUS_CHOICES,
    #reporter = models.ForeignKey(
    #name = models.CharField( max_length=200,
    #problem_description = models.TextField(
    #product_text = models.TextField(
    #product_code = models.CharField( max_length=500,
    #country = models.ForeignKey(

    # BarrierReporter fields
    #name = models.CharField(_('Reporter name'), max_length=1500, blank=True)
    #company = models.CharField(_('Company name'), max_length=1500, blank=True)

#class ReportBarrierForm(forms.ModelForm):
#    class Meta:
#        model = BarrierReport
#        fields = ['name', 'company']

class ReportBarrierStep1Form(forms.Form):
    # fields go across both BarrierReporter and BarrierReporterOrganisation
    # so we can't use a classic ModelForm (I think??)
    name_field = forms.CharField(label=_('Your name'), required=False)
    CHOICES = (('', 'First',), ('2', 'Second',))
    org_type_field = forms.ChoiceField(
        label='',
        #widget=forms.RadioSelect(attrs={'class' : 'form-control'}),
        widget=forms.RadioSelect(),
        choices=BarrierReporterOrganisation.BARRIER_REPORTER_ORGTYPE_CHOICES,
        required=False
    )
    role_field = forms.CharField(label=_('Your role / job title'), required=False)
    email_address_field = forms.EmailField(label=_('Email address'), required=False)
    telephone_number_field = forms.CharField(label=_('Contact telephone number'), required=False)

    #your_name
    #exporter_or_trade_associaion
    #role_job_title
    #email_address
    #telephone_number

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        return super(ReportBarrierStep1Form, self).__init__(*args, **kwargs)

    # condition method for WizardView
    def is_complete(wizard):
        return True


class ReportBarrierStep2Form(forms.Form): 
    organisation_name_field = forms.CharField()
    companies_house_record = forms.CharField()
    not_registered_with_companies_house = forms.CharField()
    organisation_name_freetext_field = forms.CharField()
    address_first_line_city_freetext_field = forms.CharField()
    postcode_freetext_field = forms.CharField()

    # condition method for WizardView
    def is_complete(wizard):
        return True

class ReportBarrierStep3Form(forms.Form): 
    product_text_field = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
    product_codes_field = forms.CharField(
        required=False
    )
    countries_field = forms.CharField()
    problem_description_field = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
    OTHER_MARKETS_CHOICES = ((True, 'Yes',), (False, 'No',))
    other_markets_field = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(),
        choices=OTHER_MARKETS_CHOICES,
        required=False
    )
    export_to_other_countries_description_field = forms.CharField(
        widget=forms.Textarea
    )
    impact_you_would_expect_field = forms.CharField(
        required=False
    )
    annual_turnover_field = forms.CharField(
        required=False
    )
    problem_duration_field = forms.CharField(
        required=False
    )
    OTHER_COMPANIES_AFFECTED_CHOICES = (
        ('Yes', 'Yes',),
        ('No', 'No',),
        ('Don\'t Know', 'Don\'t Know',),
    )
    other_companies_affected_field = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(),
        choices=OTHER_COMPANIES_AFFECTED_CHOICES,
        required=False
    )

    # condition method for WizardView
    def is_complete(wizard):
        return True

class ReportBarrierStep4Form(forms.Form): 
    # just has barrier type selector - TBD
    pass

    # condition method for WizardView
    def is_complete(wizard):
        return True


class ReportBarrierStep5Form(forms.Form): 
    steps_taken_field = forms.CharField(
        widget=forms.Textarea(attrs={'rows':5}),
        required=False
    )
    how_likely_to_be_resolved_field = forms.CharField(
        widget=forms.Textarea(attrs={'rows':5}),
        required=False
    )
    DESIRED_SUPPORT_NONE = 'None'
    DESIRED_SUPPORT_LOCAL = 'Local'
    DESIRED_SUPPORT_BROAD = 'Broad'
    DESIRED_SUPPORT_NOT_SURE = 'Not Sure'
    DESIRED_SUPPORT_CHOICES = (
        (DESIRED_SUPPORT_NONE, 'None - this is for your information only',),
        (DESIRED_SUPPORT_LOCAL, 'Local engagement only with UK government officials in the country I am trying to export to',),
        (DESIRED_SUPPORT_BROAD, 'Broader UK government involvement',),
        (DESIRED_SUPPORT_NOT_SURE, 'Not sure',),
    )
    desired_support_field = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(),
        choices=DESIRED_SUPPORT_CHOICES,
        required=False
    )
    confidentiality_issues_field = forms.CharField(
        widget=forms.Textarea(attrs={'rows':5}),
        required=False
    )
    PUBLISH_CONSENT_YES = 'Yes'
    PUBLISH_CONSENT_NO = 'No'
    PUBLISH_CONSENT_CONSULT_ME = 'Consult me first'
    PUBLISH_CONSENT_CHOICES = (
        (PUBLISH_CONSENT_YES, 'Yes, I give my permission',),
        (PUBLISH_CONSENT_NO, 'No, I don’t give my permission',),
        (PUBLISH_CONSENT_CONSULT_ME, 'Don\'t publish before consulting me',),
    )
    desired_support_field = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(),
        choices=DESIRED_SUPPORT_CHOICES,
        required=False
    )

    # condition method for WizardView
    def is_complete(wizard):
        return True

class ReportBarrierStep6Form(forms.Form): 
    any_other_details_field = forms.CharField(
        widget=forms.Textarea(attrs={'rows':5}),
        required=False
    )

    # condition method for WizardView
    def is_complete(wizard):
        return True

class ReportBarrierStep7Form(forms.Form): 
    pass

    # condition method for WizardView
    def is_complete(wizard):
        return True

class ReportBarrierRegisterForm(forms.Form): 
    pass

    # condition method for WizardView
    def is_complete(wizard):
        return True
