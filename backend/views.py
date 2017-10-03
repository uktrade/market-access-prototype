from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from barriers.models import MarketAccessBarrier

class DashboardView(ListView):
    model = MarketAccessBarrier
    template_name = 'backend/dashboard.html'
    pass

class ReportHomeView(ListView):
    model = MarketAccessBarrier
    template_name = 'backend/report-home.html'
    pass
