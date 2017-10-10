""" barriers/urls.py

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
"""
from django.conf.urls import url  # , include
# from django.views import generic

from .views import (
    HomeView,
    BarriersCheckResultsView,
    ReportBarrierView, ReportBarrierExistingView, ReportBarrierShowCurrentBarriersView, ReportBarrierFormView,
    BarrierDetailView, BarrierDetailStaticView, BarrierExtraDetailView, BarrierSubscribeView,
    ReportBarrierStep1View, ReportBarrierStep2View, ReportBarrierStep3View,
    ReportBarrierStep4View, ReportBarrierStep5View, ReportBarrierStep6View,
    ReportBarrierRegisterView,
    BarriersGeneralInfoView,
    BarriersCaseStudyView, BarriersCaseStudy2View, BarriersCaseStudy3View,
    RequestFastTrackView, FastTrackPhoneTextView,
    ExampleSummaryView,
    CompaniesHouseRequestView
)

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    #url(r'^barriers/check/form',
    #    BarriersCheckFormView.as_view(),
    #    name='barriers-check-form'
    #),
    url(r'^barriers/check/results',
        BarriersCheckResultsView.as_view(),
        name='barriers-check-results'
    ),
    url(r'^barrier/subscribe',
        BarrierSubscribeView.as_view(),
        name='barrier-subscribe'
    ),
    url(r'^barriers/(?P<pk>[\d]+)/detail',
        BarrierDetailStaticView.as_view(),
        name='barrier-detail-static'
    ),
    url(r'^barriers/extra-detail',
        BarrierExtraDetailView.as_view(),
        name='barrier-extra-detail'
    ),
    url(r'^barriers/(?P<pk>\w+)/report',
        ReportBarrierExistingView.as_view(),
        name='report-barrier-existing'
    ),
    url(r'^barriers/(?P<pk>\d+)',
        BarrierDetailView.as_view(),
        name='barrier-detail'
    ),
    url(r'^report/show-current-barriers/countries/(?P<countries>\w+)',
        ReportBarrierShowCurrentBarriersView.as_view(),
        name='report-barrier-show-current-barriers'
    ),
    url(r'^barriers/general-info',
        BarriersGeneralInfoView.as_view(),
        name='barriers-general-info'
    ),
    url(r'^barriers/case-study-1',
        BarriersCaseStudyView.as_view(),
        name='barriers-case-study'
    ),
    url(r'^barriers/case-study-2',
        BarriersCaseStudy2View.as_view(),
        name='barriers-case-study-2'
    ),
    url(r'^barriers/case-study-3',
        BarriersCaseStudy3View.as_view(),
        name='barriers-case-study-3'
    ),
    url(r'^report/step1',
        ReportBarrierStep1View.as_view(),
        name='report-barrier-step1'
    ),
    url(r'^report/step2',
        ReportBarrierStep2View.as_view(),
        name='report-barrier-step2'
    ),
    url(r'^report/step3',
        ReportBarrierStep3View.as_view(),
        name='report-barrier-step3'
    ),
    url(r'^report/step4',
        ReportBarrierStep4View.as_view(),
        name='report-barrier-step4'
    ),
    url(r'^report/step5',
        ReportBarrierStep5View.as_view(),
        name='report-barrier-step5'
    ),
    url(r'^report/step6',
        ReportBarrierStep6View.as_view(),
        name='report-barrier-step6'
    ),
    url(r'^report/register',
        ReportBarrierRegisterView.as_view(),
        name='report-barrier-register'
    ),
    url(r'^report/form',
        ReportBarrierFormView.as_view(),
        name='report-barrier-form'
    ),
    url(r'^barriers/notifications/(?P<pk>\w+)/report',
        ReportBarrierExistingView.as_view(),
        name='report-notification-existing'
    ),
    url(r'^report',
        ReportBarrierView.as_view(),
        name='report-barrier'
    ),
    url(r'^request-fast-track',
         RequestFastTrackView.as_view(),
        name='request-fast-track'
    ),
    url(r'^fast-track-phone-text',
        FastTrackPhoneTextView.as_view(),
        name='fast-track-phone-text'
    ),
    url(r'^summary',
        ExampleSummaryView.as_view(),
        name='example-summary'
    ),
    url(r'^api/companieshouse',
        CompaniesHouseRequestView.as_view(),
        name='companies-house-lookup'
    ),
]
