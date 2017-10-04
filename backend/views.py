from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from barriers.models import BarrierReport

class IndexView(ListView):
    model = BarrierReport
    template_name = 'backend/_index.html'
    pass

class ComponentsView(ListView):
    model = BarrierReport
    template_name = 'backend/_all-elements.html'
    pass

class DashboardView(ListView):
    model = BarrierReport
    template_name = 'backend/dashboard.html'
    pass

class DashboardSuccessView(ListView):
    model = BarrierReport
    template_name = 'backend/dashboard-success.html'
    pass


class ReportHomeView(ListView):
    model = BarrierReport
    template_name = 'backend/report-home.html'
    pass

class ReportBarrierTypeView(ListView):
    model = BarrierReport
    template_name = 'backend/report-barrier-type.html'
    pass

class ReportHomeMakeADecisionView(ListView):
    model = BarrierReport
    template_name = 'backend/report-home-make-a-decision.html'
    pass

class ReportBarrierMakeADecisionView(ListView):
    model = BarrierReport
    template_name = 'backend/report-barrier-make-a-decision.html'
    pass

class ReportHomeDecisionMadeView(ListView):
    model = BarrierReport
    template_name = 'backend/report-home-decision-made.html'
    pass

class ReportCreateBarrierView(ListView):
    model = BarrierReport
    template_name = 'backend/report-create-barrier.html'
    pass

class ReportNewUKView(ListView):
    model = BarrierReport
    template_name = 'backend/report-new-uk.html'
    pass

class ReportNewInstanceView(ListView):
    model = BarrierReport
    template_name = 'backend/report-new-instance.html'
    pass

class ReportHomeBarrierCreatedView(ListView):
    model = BarrierReport
    template_name = 'backend/report-home-barrier-created.html'
    pass

class ReportAssignLeadView(ListView):
    model = BarrierReport
    template_name = 'backend/report-assign-lead.html'
    pass

class ReportAssignLeadSearchResultsView(ListView):
    model = BarrierReport
    template_name = 'backend/report-assign-lead-search-results.html'
    pass

class ReportHomeReadyToProceedCreatedView(ListView):
    model = BarrierReport
    template_name = 'backend/report-home-ready-to-proceed.html'
    pass

class ReportHomeProceedToAssessmentView(ListView):
    model = BarrierReport
    template_name = 'backend/report-home-proceed-to-assessment.html'
    pass

class InviteLeadTimePassesView(ListView):
    model = BarrierReport
    template_name = 'backend/invite-lead-time-passes.html'
    pass
