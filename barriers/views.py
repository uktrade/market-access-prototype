# marketaccess/views.py

import json
import requests

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
from .models import BarrierRecord, BarrierSource, BarrierCountry
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

    def get_success_url(self, **kwargs):
        return reverse_lazy(
                    'report-barrier-show-current-barriers',
                    kwargs= { 'countries' : self.countries }
               )

    def form_valid(self, form):
        self.countries = form.cleaned_data['countries_affected']
        return super(ReportBarrierView, self).form_valid(form)

class ReportBarrierExistingView(FormView):
    template_name = 'report-barrier-existing.html'
    form_class = BarrierCountryForm

    countries = ''

    def get_success_url(self, **kwargs):
        return reverse_lazy(
                    'report-barrier-show-current-barriers',
                    kwargs= { 'countries' : self.countries }
               )

    def form_valid(self, form):
        self.countries = form.cleaned_data['countries_affected']
        return super(ReportBarrierView, self).form_valid(form)

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


class ReportBarrierFormView(FormView):
    template_name = 'report-barrier-form.html'
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


class BarriersByCountryView(ListView):
    template_name = 'barriers-by-country.html'
    country = ''
    model = BarrierRecord

    def dispatch(self, request, *args, **kwargs):
        self.country_text = kwargs['country']
        return super(BarriersByCountryView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        uk_source = BarrierSource.objects.get(short_name='UK')
        self.country_object = BarrierCountry.objects.get(name=self.country_text)
        return BarrierRecord.objects.filter(country=self.country_object).filter(barrier_source=uk_source)

    def get_context_data(self, **kwargs):
        context_data =  super(BarriersByCountryView, self).get_context_data(**kwargs)
        context_data['country'] = self.country_text
        # "objects" will be UK barriers, make "wto_barriers"
        # and "ec_barriers" contain the appropriate ones
        wto_source = BarrierSource.objects.get(short_name='WTO')
        ec_source = BarrierSource.objects.get(short_name='EC MADB')
        context_data['wto_barriers'] = BarrierRecord.objects.filter(country=self.country_object).filter(barrier_source=wto_source)
        context_data['ec_barriers'] = BarrierRecord.objects.filter(country=self.country_object).filter(barrier_source=ec_source)
        return context_data


class BarrierDetailView(DetailView):
    model = BarrierRecord
    template_name = 'barrier-detail.html'


class SessionContextMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(SessionContextMixin, self).get_context_data(*args, **kwargs)
        if 'existing' in self.request.session:
            context['existing'] = self.request.session['existing']
        if 'is_trade_association' in self.request.session:
            context['is_trade_association'] = self.request.session['is_trade_association']
        return context


class BarrierDetailStaticView(TemplateView):
    model = BarrierRecord
    template_name = 'barrier-detail-static.html'

class BarrierExtraDetailView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'barrier-extra-detail.html'

class BarrierSubscribeView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'barrier-subscribe.html'

class BarriersGeneralInfoView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'barriers-general-info.html'

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

    def get(self, request, *args, **kwargs):
        if 'existing' in request.GET:
            request.session['existing'] = request.GET['existing']
        return super(ReportBarrierStep1View, self).get(request, *args, **kwargs)


class ReportBarrierStep2View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-step2.html'

    def post(self, request, *args, **kwargs):
        if 'dit[step1][type]' in self.request.POST:
            if request.POST['dit[step1][type]'] == 'I work for a trade association':
                request.session['is_trade_association'] = True
            else:
                # Allow it to be turned off again
                request.session['is_trade_association'] = False
        return self.get(request, *args, **kwargs)


class ReportBarrierStep3View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-step3.html'

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
