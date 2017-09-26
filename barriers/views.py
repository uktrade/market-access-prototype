# marketaccess/views.py

import json
import requests

from django.conf import settings
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.urls import reverse_lazy

from api_client import api_client
from .helpers import (
    store_companies_house_profile_in_session_and_validate,
    has_company
)
from .models import MarketAccessBarrier
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
        context['num_barriers'] = MarketAccessBarrier.objects.count
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

class ReportBarrierShowCurrentBarriersView(ListView):
    template_name = 'report-barrier-show-current-barriers.html'
    countries_affected = ''
    model = MarketAccessBarrier

    def dispatch(self, request, *args, **kwargs):
        self.countries_affected = kwargs['countries']
        return super(ReportBarrierShowCurrentBarriersView, self).dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return MarketAccessBarrier.objects.filter(notifying_member=self.countries_affected)

    def get_context_data(self, **kwargs):
        context_data =  super(ReportBarrierShowCurrentBarriersView, self).get_context_data(**kwargs)
        context_data['countries_affected'] = self.countries_affected
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
    model = MarketAccessBarrier

    def dispatch(self, request, *args, **kwargs):
        self.country = kwargs['country']
        return super(BarriersByCountryView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return MarketAccessBarrier.objects.filter(notifying_member=self.country)

    def get_context_data(self, **kwargs):
        context_data =  super(BarriersByCountryView, self).get_context_data(**kwargs)
        context_data['country'] = self.country
        return context_data

class PostGetTemplateView(TemplateView):
    def post(self, *args, **kwargs):
        if 'dit[step1][type]' in self.request.POST:
            if self.request.POST['dit[step1][type]'] == 'I work for a trade association':
                self.request.session['is_trade_association'] = True
            else:
                # Allow it to be turned off again
                self.request.session['is_trade_association'] = False
        return self.get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(PostGetTemplateView, self).get_context_data(*args, **kwargs)
        if 'is_trade_association' in self.request.session:
            context['is_trade_association'] = self.request.session['is_trade_association']
        return context

class BarrierDetailView(DetailView):
    model = MarketAccessBarrier
    template_name = 'barrier-detail.html'

class BarrierDetailStaticView(TemplateView):
    model = MarketAccessBarrier
    template_name = 'barrier-detail-static.html'

class BarrierSubscribeView(TemplateView):
    model = MarketAccessBarrier
    template_name = 'barrier-subscribe.html'

class BarriersGeneralInfoView(TemplateView):
    model = MarketAccessBarrier
    template_name = 'barriers-general-info.html'

class BarriersCaseStudyView(TemplateView):
    model = MarketAccessBarrier
    template_name = 'barriers-case-study.html'

class ReportBarrierStep1View(PostGetTemplateView):
    model = MarketAccessBarrier
    template_name = 'report-barrier-step1.html'

class ReportBarrierStep2View(PostGetTemplateView):
    model = MarketAccessBarrier
    template_name = 'report-barrier-step2.html'

class ReportBarrierStep3View(PostGetTemplateView):
    model = MarketAccessBarrier
    template_name = 'report-barrier-step3.html'

class ReportBarrierStep4View(PostGetTemplateView):
    model = MarketAccessBarrier
    template_name = 'report-barrier-step4.html'

class ReportBarrierStep5View(PostGetTemplateView):
    model = MarketAccessBarrier
    template_name = 'report-barrier-step5.html'

class ReportBarrierStep6View(PostGetTemplateView):
    model = MarketAccessBarrier
    template_name = 'report-barrier-step6.html'

class ReportBarrierRegisterView(PostGetTemplateView):
    model = MarketAccessBarrier
    template_name = 'report-barrier-register.html'

class RequestFastTrackView(TemplateView):
    model = MarketAccessBarrier
    template_name = 'request-fast-track.html'


class CompaniesHouseRequestView(TemplateView):
    template_name = 'companies-house-api.html'
    search_company = ''

    def dispatch(self, request, *args, **kwargs):
        self.search_company = request.GET.get('company', '')
        return super(CompaniesHouseRequestView, self).dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **kwargs):
        url = ('https://api.companieshouse.gov.uk/search/companies'
                         '?items_per_page=10&q={}'.format(self.search_company))
        api_response = requests.get(url,
                         auth=(settings.COMPANIES_HOUSE_API_KEY, ''))
        kwargs['content_type'] = 'application/json'
        return HttpResponse(api_response.text, **kwargs)
