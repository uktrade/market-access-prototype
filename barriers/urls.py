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
    ReportBarrierView, ReportBarrierShowCurrentBarriersView, ReportBarrierFormView,
    BarrierDetailView, BarrierSubscribeView, BarriersByCountryView,
    ReportBarrierStep1View, ReportBarrierStep2View, ReportBarrierStep3View,
    ReportBarrierStep4View, ReportBarrierStep5View, ReportBarrierStep6View,
    ReportBarrierRegisterView,
    BarriersGeneralInfoView, BarriersCaseStudyView,
    RequestFastTrackView
)

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^barriers/countries/(?P<country>\w+)',
        BarriersByCountryView.as_view(),
        name='barriers-by-country'
    ),
    url(r'^barrier/subscribe',
        BarrierSubscribeView.as_view(),
        name='barrier-subscribe'
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
    url(r'^barriers/case-study',
        BarriersCaseStudyView.as_view(),
        name='barriers-case-study'
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
    url(r'^report',
         ReportBarrierView.as_view(),
        name='report-barrier'
    ),
    url(r'^request-fast-track',
         RequestFastTrackView.as_view(),
        name='request-fast-track'
    ),
]
