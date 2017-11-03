# marketaccess/views.py

import json
import requests
from mptt.templatetags.mptt_tags import cache_tree_children

from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
from django.shortcuts import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    View, TemplateView, FormView, ListView, DetailView
)

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

class GovUKView(TemplateView):
    template_name = 'govuk.html'
    pass

class GovUKDITView(TemplateView):
    template_name = 'govuk-dit.html'
    pass

class PrototypesView(TemplateView):
    template_name = 'prototypes.html'
    pass

class ReportBarrierView(FormView):
    template_name = 'report-barrier.html'
    form_class = BarrierCountryForm

    countries = ''

    def get(self, request, *args, **kwargs):
        # we're reporting a new barrier, so clear
        # any existing barriers from the session
        if 'existingbarrier' in request.session:
            del request.session['existingbarrier']
        if 'existingnotification' in request.session:
            del request.session['existingnotification']
        return super(ReportBarrierView, self).get(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy(
                    'home'
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
                    'home'
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
                    'home'
               )

    def form_valid(self, form):
        self.countries = form.cleaned_data['countries_affected']
        return super(ReportExistingNotificationView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ReportExistingNotificationView, self).get_context_data(*args, **kwargs)
        context['barrier'] = self.notification
        return context


class SearchView(FormView):
    template_name = 'search.html'
    form_class = ReportBarrierForm

    countries = ''

    def get_success_url(self, **kwargs):
        return reverse_lazy(
                    'home'
               )

    def form_valid(self, form):
        self.countries = form.cleaned_data['countries_affected']
        return super(SearchView, self).form_valid(form)


class SearchResultsView(ListView):
    template_name = 'search-results.html'
    country_text = ''
    country_object = None
    model = BarrierRecord
    context_object_name = 'uk_barriers'
    paginate_by = 10 # page size for default queryset ie UK barrier reports
    EC_NOTIFICATIONS_PAGE_SIZE = 5
    WTO_NOTIFICATIONS_PAGE_SIZE = 5

    def __init__(self, *args, **kwargs):
        self.uk_source = BarrierSource.objects.get(short_name='UK')
        #self.wto_source = BarrierSource.objects.get(short_name='WTO')
        self.ec_source = BarrierSource.objects.get(short_name='EC MADB')
        return super(SearchResultsView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.countries_search_text = request.GET.getlist('countries')
        self.product_search_text = request.GET.get('s', None)
        self.sector_search_text = request.GET.get('sectors', None)
        self.commoditycode_search_text = request.GET.get('commoditycodes', None)
        self.uk_barriers_page_number = kwargs.get('page', 1)
        return super(SearchResultsView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        self.uk_barriers = BarrierRecord.objects.order_by('pk')  # BarrierRecord doesn't need to be filtered
        self.ec_notifications = BarrierNotification.objects.filter(barrier_source=self.ec_source).order_by('pk')
        if self.countries_search_text:
            countries = []
            try:
                for country in self.countries_search_text:
                    country_object = BarrierCountry.objects.get(name__iexact=country)
                    countries.append(country_object)
            except BarrierCountry.DoesNotExist:
                self.uk_barriers = []
                self.ec_notifications = []
            else:
                self.uk_barriers = self.uk_barriers.filter(country__in=countries)
                self.ec_notifications = self.ec_notifications.filter(country__in=countries)
        if self.product_search_text:
            self.uk_barriers = self.uk_barriers.filter(
                Q(title__icontains=self.product_search_text)
                | Q(description__icontains=self.product_search_text)
            )
            self.ec_notifications = self.ec_notifications.filter(
                Q(title__icontains=self.product_search_text)
                | Q(description__icontains=self.product_search_text)
                | Q(products_text__icontains=self.product_search_text)
            )
        return self.uk_barriers

    def get_context_data(self, **kwargs):
        context_data =  super(SearchResultsView, self).get_context_data(**kwargs)
        context_data['countries'] = self.countries_search_text
        context_data['products'] = self.product_search_text
        context_data['sector'] = self.sector_search_text
        # uk_barriers will be created by default
        context_data['ec_notifications'] = Paginator(self.ec_notifications, self.EC_NOTIFICATIONS_PAGE_SIZE).page(1)
        #context_data['wto_barriers'] = Paginator(self.wto_barriers, self.WTO_NOTIFICATIONS_PAGE_SIZE).page(1)
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
        if 'logged_in' in self.request.session:
            context['logged_in'] = self.request.session['logged_in']
        return context


class NotificationDetailView(DetailView):
    model = BarrierNotification
    template_name = 'notification-detail.html'

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
        uk_source = BarrierSource.objects.get(short_name='UK')
        return BarrierType.objects.filter(barrier_source=uk_source)

class BarriersCaseStudyView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'barriers-case-study1.html'

class BarriersCaseStudy2View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'barriers-case-study2.html'

class BarriersCaseStudy3View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'barriers-case-study3.html'

class ReportBarrierTaskListView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-task-list.html'

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
            elif 'is_trade_association' in request.session:
                # Allow it to be turned off again
                del request.session['is_trade_association']
        return self.get(request, *args, **kwargs)


class ReportBarrierStep3View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-step3.html'

class ReportBarrierStep4View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-step4.html'
    # https://django-mptt.github.io/django-mptt/tutorial.html#template

    def get_context_data(self, *args, **kwargs):
        context = super(ReportBarrierStep4View, self).get_context_data(*args, **kwargs)
        # warning - this will need to change if we change
        # the code of the UK barrier source
        uk_source = BarrierSource.objects.get(short_name='UK')
        uk_barrier_types = BarrierType.objects.filter(barrier_source=uk_source)
        context['barrier_types'] = uk_barrier_types
        return context

class ReportBarrierStep5View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-step5.html'

class ReportBarrierStep6View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-step6.html'

class ReportBarrierStep7View(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-step7.html'

class ReportBarrierRegisterView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-register.html'

class ReportBarrierLoginView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-login.html'

class ReportBarrierLogoutView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-logout.html'

    def dispatch(self, request, *args, **kwargs):
        if 'logged_in' in request.session:
            request.session['logged_in'] = False
        return super(ReportBarrierLogoutView, self).dispatch(request, *args, **kwargs)

class ReportBarrierSaveView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-save.html'

    def dispatch(self, request, *args, **kwargs):
        if 'logged_in' in request.GET:
            request.session['logged_in'] = True
        return super(ReportBarrierSaveView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReportBarrierSaveView, self).get_context_data(**kwargs)
        context['logged_in'] = 'false'
        context['completed_1'] = 'false'
        context['completed_2'] = 'false'
        context['completed_3'] = 'false'
        context['completed_4'] = 'false'
        context['completed_5'] = 'false'
        context['completed_6'] = 'false'

        if context['step'] == '1':
          context['completed_1'] = 'true'
        elif context['step'] == '2':
          context['completed_1'] = 'true'
          context['completed_2'] = 'true'
        elif context['step'] == '3':
          context['completed_1'] = 'true'
          context['completed_2'] = 'true'
          context['completed_3'] = 'true'
        elif context['step'] == '4':
          context['completed_1'] = 'true'
          context['completed_2'] = 'true'
          context['completed_3'] = 'true'
          context['completed_4'] = 'true'
        elif context['step'] == '5':
          context['completed_1'] = 'true'
          context['completed_2'] = 'true'
          context['completed_3'] = 'true'
          context['completed_4'] = 'true'
          context['completed_5'] = 'true'
        elif context['step'] == '6':
          context['completed_1'] = 'true'
          context['completed_2'] = 'true'
          context['completed_3'] = 'true'
          context['completed_4'] = 'true'
          context['completed_5'] = 'true'
          context['completed_6'] = 'true'

        context['logged_in'] = self.request.session['logged_in']
        return context

class ReportBarrierSuccessView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'report-barrier-success.html'

class RequestFastTrackView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'request-fast-track.html'

class FastTrackPhoneTextView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'fast-track-phone-text.html'

class ExampleSummaryView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'example-summary.html'

class ThanksView(SessionContextMixin, TemplateView):
    model = BarrierRecord
    template_name = 'thanks.html'


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



class BarrierSubtypesLookupView(View):
    def get(self, request, *args, **kwargs):
        self.barrier_type = request.GET.get('barrier_type', '')
        api_response = ''
        if self.barrier_type:
            tree_node = BarrierType.objects.get(pk=self.barrier_type)
            tree_children_dict= tree_node.children_as_dict()
            kwargs['content_type'] = 'application/json'
            api_response = json.dumps(tree_children_dict)
        return HttpResponse(api_response, **kwargs)
