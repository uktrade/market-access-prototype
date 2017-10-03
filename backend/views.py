from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from barriers.models import BarrierReport

class DashboardView(ListView):
    model = BarrierReport
    template_name = 'backend/dashboard.html'
    pass

class ReportHomeView(ListView):
    model = BarrierReport
    template_name = 'backend/report-home.html'
    pass
