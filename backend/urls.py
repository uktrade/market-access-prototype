""" backend/urls.py

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
    IndexView,
    ComponentsView,
    DashboardView,
    DashboardSuccessView,
    # Screen, find lead, and proceed
    ReportHomeView,
    ReportBarrierTypeView,
    ReportHomeMakeADecisionView,
    ReportBarrierMakeADecisionView,
    ReportHomeDecisionMadeView,
    ReportCreateBarrierView,
    ReportNewUKView,
    ReportNewInstanceView,
    ReportHomeBarrierCreatedView,
    ReportAssignLeadView,
    ReportAssignLeadSearchResultsView,
    ReportHomeReadyToProceedCreatedView,
    ReportHomeProceedToAssessmentView,
    InviteLeadTimePassesView,
    # Assess and manage
    BarrierHomeView
)

urlpatterns = [
    url(r'^index$',
        IndexView.as_view(),
        name='index'
    ),
    url(r'^components$',
        ComponentsView.as_view(),
        name='components'
    ),
    url(r'^$',
        DashboardView.as_view(),
        name='dashboard'
    ),
    url(r'^success$',
        DashboardSuccessView.as_view(),
        name='dashboard-success'
    ),
    # Screen, find lead, and proceed
    url(r'^report-home$',
        ReportHomeView.as_view(),
        name='report-home'
    ),
    url(r'^report-barrier-type$',
        ReportBarrierTypeView.as_view(),
        name='report-barrier-type'
    ),
    url(r'^report-home/make-a-decision$',
        ReportHomeMakeADecisionView.as_view(),
        name='report-home-make-a-decision'
    ),
    url(r'^report-barrier/make-a-decision$',
        ReportBarrierMakeADecisionView.as_view(),
        name='report-barrier-make-a-decision'
    ),
    url(r'^report-home/decision-made$',
        ReportHomeDecisionMadeView.as_view(),
        name='report-home-decision-made'
    ),
    url(r'^report-create-barrier$',
        ReportCreateBarrierView.as_view(),
        name='report-create-barrier'
    ),
    url(r'^report-new-uk$',
        ReportNewUKView.as_view(),
        name='report-new-uk'
    ),
    url(r'^report-new-instance$',
        ReportNewInstanceView.as_view(),
        name='report-new-instance'
    ),
    url(r'^report-home/barrier-created$',
        ReportHomeBarrierCreatedView.as_view(),
        name='report-home-barrier-created'
    ),
    url(r'^report/assign-lead$',
        ReportAssignLeadView.as_view(),
        name='report-assign-lead'
    ),
    url(r'^report/assign-lead/search-results$',
        ReportAssignLeadSearchResultsView.as_view(),
        name='report-assign-lead-search-results'
    ),
    url(r'^report-home/ready-to-proceed$',
        ReportHomeReadyToProceedCreatedView.as_view(),
        name='report-home-ready-to-proceed'
    ),
    url(r'^report-home/proceed-to-assessment$',
        ReportHomeProceedToAssessmentView.as_view(),
        name='report-home-proceed-to-assessment'
    ),
    url(r'^invite-lead-time-passes$',
        InviteLeadTimePassesView.as_view(),
        name='invite-lead-time-passes'
    ),
    # Assess and manage
    url(r'^barrier-home$',
        BarrierHomeView.as_view(),
        name='barrier-home'
    ),
]
