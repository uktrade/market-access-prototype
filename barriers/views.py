# marketaccess/views.py

import json
import requests

from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import HttpResponse
from django.views.generic import (
    View, TemplateView, FormView, ListView, DetailView
)
from django.urls import reverse_lazy

from api_client import api_client
from .helpers import (
    store_companies_house_profile_in_session_and_validate,
    has_company
)
from .models import (
    BarrierNotification, BarrierRecord, BarrierSource,
    BarrierReport, BarrierCountry, BarrierType
)
from .forms import BarrierCountryForm, ReportBarrierForm

from sso.utils import SSOSignUpRequiredMixin

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        user = self.request.sso_user
        context['user'] = user
        context['user_has_company'] = (
            user and has_company(user.session_id)
        )
        context['num_barriers'] = BarrierRecord.objects.count
        return context

class ReportBarrierView(FormView):
    template_name = 'report-barrier.html'
    form_class = BarrierCountryForm

    countries = ''

    def get(self, request, *args, **kwargs):
        # we're reporting a new barrier, so clear
        # any existing barriers from the session
        if 'existingbarrier' in request.session:
            del request.session['existingbarrier']
        return super(ReportBarrierView, self).get(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy(
                    'report-barrier-show-current-barriers',
                    kwargs= { 'countries' : self.countries }
               )

    def form_valid(self, form):
        self.countries = form.cleaned_data['countries_affected']
        return super(ReportBarrierView, self).form_valid(form)


class ReportExistingBarrierView(FormView):
    template_name = 'report-barrier-existing.html'
    form_class = BarrierCountryForm

    countries = ''

    def get(self, request, *args, **kwargs):
        self.barrier = BarrierRecord.objects.get(pk = kwargs['pk'])
        request.session['existingbarrier'] = self.barrier.pk
        if 'existingnotification' in request.session:
            del request.session['existingnotification']
        return super(ReportExistingBarrierView, self).get(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy(
                    'report-barrier-show-current-barriers',
                    kwargs= { 'countries' : self.countries }
               )

    def form_valid(self, form):
        self.countries = form.cleaned_data['countries_affected']
        return super(ReportExistingBarrierView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ReportExistingBarrierView, self).get_context_data(*args, **kwargs)
        context['barrier'] = self.barrier
        return context


class ReportExistingNotificationView(FormView):
    template_name = 'report-barrier-existing.html'
    form_class = BarrierCountryForm

    countries = ''

    def get(self, request, *args, **kwargs):
        self.notification = BarrierNotification.objects.get(pk = kwargs['pk'])
        request.session['existingnotification'] = self.notification.pk
        if 'existingbarrier' in request.session:
            del request.session['existingbarrier']
        return super(ReportExistingNotificationView, self).get(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy(
                    'report-barrier-show-current-barriers',
                    kwargs= { 'countries' : self.countries }
               )

    def form_valid(self, form):
        self.countries = form.cleaned_data['countries_affected']
        return super(ReportExistingNotificationView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ReportExistingNotificationView, self).get_context_data(*args, **kwargs)
        context['barrier'] = self.notification
        return context



class ReportBarrierShowCurrentBarriersView(ListView):
    template_name = 'report-barrier-show-current-barriers.html'
    country = ''
    model = BarrierRecord

    def dispatch(self, request, *args, **kwargs):
        self.country = kwargs['countries']
        return super(ReportBarrierShowCurrentBarriersView, self).dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        db_country = BarrierCountry.objects.get(name=self.country)
        return BarrierRecord.objects.filter(country=db_country)

    def get_context_data(self, **kwargs):
        context_data =  super(ReportBarrierShowCurrentBarriersView, self).get_context_data(**kwargs)
        context_data['countries_affected'] = self.db_country.name
        return context_data


class CheckBarriersFormView(FormView):
    template_name = 'check-barriers-form.html'
    form_class = ReportBarrierForm

    countries = ''

    def get_success_url(self, **kwargs):
        return reverse_lazy(
                    'report-barrier-show-current-barriers',
                    kwargs= { 'countries' : self.countries }
               )

    def form_valid(self, form):
        self.countries = form.cleaned_data['countries_affected']
        return super(ReportBarrierView, self).form_valid(form)


class CheckBarriersResultsView(ListView):
    template_name = 'barriers-check-results.html'
    country_text = ''
    country_object = None
    model = BarrierRecord
    context_object_name = 'uk_barriers'
    paginate_by = 10 # page size for default queryset ie UK barrier reports
    EC_BARRIERS_PAGE_SIZE = 5
    WTO_BARRIERS_PAGE_SIZE = 5

    def __init__(self, *args, **kwargs):
        self.uk_source = BarrierSource.objects.get(short_name='UK')
        #self.wto_source = BarrierSource.objects.get(short_name='WTO')
        self.ec_source = BarrierSource.objects.get(short_name='EC MADB')
        return super(CheckBarriersResultsView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.country_search_text = request.GET.get('countries', None)
        self.product_search_text = request.GET.get('products', None)
        self.sector_search_text = request.GET.get('sectors', None)
        self.commoditycode_search_text = request.GET.get('commoditycodes', None)
        self.uk_barriers_page_number = kwargs.get('page', 1)
        return super(CheckBarriersResultsView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        self.uk_barriers = BarrierRecord.objects.all()  # BarrierRecord doesn't have a source
        self.ec_barriers = BarrierNotification.objects.filter(barrier_source=self.ec_source)
        #self.wto_barriers = BarrierNotification.objects.filter(barrier_source=self.wto_source)
        if self.country_search_text:
            # FIXME currently assumes only one country in country_search_text
            self.country_object = BarrierCountry.objects.get(name__iexact=self.country_search_text)
            self.uk_barriers = self.uk_barriers.filter(country=self.country_object)
            self.ec_barriers = self.ec_barriers.filter(country=self.country_object)
            #self.wto_barriers = self.wto_barriers.filter(country=self.country_object)
        if self.product_search_text:
            self.uk_barriers = self.uk_barriers.filter(products=self.country_object)
            self.ec_barriers = self.ec_barriers.filter(country=self.country_object)
            #self.wto_barriers = self.wto_barriers.filter(country=self.country_object)
        # uk_paginator = Paginator(self.uk_barriers, 25) # Show 25 contacts per page
        return self.uk_barriers

    def get_context_data(self, **kwargs):
        context_data =  super(CheckBarriersResultsView, self).get_context_data(**kwargs)
        context_data['country'] = self.country_text
        # uk_barriers will be created by default
        context_data['ec_barriers'] = Paginator(self.ec_barriers, self.EC_BARRIERS_PAGE_SIZE).page(1)
        #context_data['wto_barriers'] = Paginator(self.wto_barriers, self.WTO_BARRIERS_PAGE_SIZE).page(1)
        return context_data


class BarrierDetailView(DetailView):
    model = BarrierRecord
    template_name = 'barrier-detail.html'


class SessionContextMixin(object):
    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SessionContextMixin, self).get_context_data(*args, **kwargs)
        if 'existingbarrier' in self.request.session:
            existing_barrier_id = self.request.session['existingbarrier']
            context['existingbarrier'] = BarrierRecord.objects.get(pk=existing_barrier_id)
        if 'existingnotification' in self.request.session:
            existing_notification_id = self.request.session['existingnotification']
            context['existingnotification'] = BarrierNotification.objects.get(pk=existing_notification_id)
        if 'is_trade_association' in self.request.session:
            context['is_trade_association'] = self.request.session['is_trade_association']
        return context


class BarrierDetailStaticView(DetailView):
    model = BarrierRecord
    template_name = 'barrier-detail-static.html'

class BarrierTypeDetailView(SessionContextMixin, DetailView):
    model = BarrierType
    template_name = 'barrier-type-detail.html'

class BarrierSubscribeView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'barrier-subscribe.html'

class BarriersGeneralInfoView(SessionContextMixin, ListView):
    model = BarrierType
    template_name = 'barriers-general-info.html'

    def get_queryset(self):
        # All UK Barrier Types excluding the "Other" category
        uk_source = BarrierSource.objects.get(short_name='UK')
        return BarrierType.objects.filter(barrier_source=uk_source).exclude(pk=122)

class BarriersCaseStudyView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'barriers-case-study1.html'

class BarriersCaseStudy2View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'barriers-case-study2.html'

class BarriersCaseStudy3View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'barriers-case-study3.html'

class ReportBarrierStep1View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-step1.html'

class ReportBarrierStep2View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-step2.html'

    def post(self, request, *args, **kwargs):
        if 'dit[step1][type]' in self.request.POST:
            if request.POST['dit[step1][type]'] == 'I work for a trade association':
                request.session['is_trade_association'] = True
            else:
                # Allow it to be turned off again
                del request.session['is_trade_association']
        return self.get(request, *args, **kwargs)


class ReportBarrierStep3View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-step3.html'
    # https://django-mptt.github.io/django-mptt/tutorial.html#template

    def get_context_data(self, *args, **kwargs):
        context = super(ReportBarrierStep3View, self).get_context_data(*args, **kwargs)
        # warning - this will need to change if we change
        # the code of the UK barrier source
        uk_source = BarrierSource.objects.get(short_name='UK')
        # exclude our tariffs category for now
        uk_barrier_types = BarrierType.objects.filter(barrier_source=uk_source).exclude(barrier_code=12)
        context['barrier_types'] = uk_barrier_types
        return context

class ReportBarrierStep4View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-step4.html'

class ReportBarrierStep5View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-step5.html'

class ReportBarrierStep6View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-step6.html'

class ReportBarrierRegisterView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-register.html'

class RequestFastTrackView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'request-fast-track.html'

class FastTrackPhoneTextView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'fast-track-phone-text.html'

class ExampleSummaryView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'example-summary.html'


class CompaniesHouseRequestView(View):
    search_company = ''

    def get(self, request, *args, **kwargs):
        self.search_company = request.GET.get('company', '')
        api_response = requests.get('https://api.companieshouse.gov.uk/search/companies'
                         '?q={}'
                         .format(self.search_company),
                         auth=(settings.COMPANIES_HOUSE_API_KEY, ''))
        kwargs['content_type'] = 'application/json'
        return HttpResponse(api_response.text, **kwargs)
