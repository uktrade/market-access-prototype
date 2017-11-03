from django.shortcuts import render
from django.views.generic import ListView, TemplateView, FormView
from barriers.models import BarrierSource, BarrierReport, BarrierType
from .forms import ChooseBarrierTypeForm

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

# Screen, find lead, and proceed
class ReportHomeView(ListView):
    model = BarrierReport
    template_name = 'backend/report-home.html'
    pass

class ReportBarrierTypeView(FormView):
    model = BarrierReport
    template_name = 'backend/report-barrier-type.html'
    form_class = ChooseBarrierTypeForm

    def get_context_data(self, *args, **kwargs):
        context = super(ReportBarrierTypeView, self).get_context_data(*args, **kwargs)
        # warning - this will need to change if we change
        # the code of the UK barrier source
        uk_source = BarrierSource.objects.get(short_name='UK')
        uk_barrier_types = BarrierType.objects.filter(barrier_source=uk_source)
        context['barrier_types'] = uk_barrier_types
        return context

class ReportBarrierTypeChildView(FormView):
    model = BarrierReport
    template_name = 'backend/report-barrier-type-child.html'
    form_class = ChooseBarrierTypeForm

    def get_context_data(self, *args, **kwargs):
        context = super(ReportBarrierTypeChildView, self).get_context_data(*args, **kwargs)
        # warning - this will need to change if we change
        # the code of the UK barrier source
        uk_source = BarrierSource.objects.get(short_name='UK')
        uk_barrier_types = BarrierType.objects.filter(barrier_source=uk_source)
        context['barrier_types'] = uk_barrier_types
        context['barrier_types_children'] = uk_barrier_types
        return context

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

class ReportCreateBarrierView(FormView):
    model = BarrierReport
    template_name = 'backend/report-create-barrier.html'

    def get_form(self, *args, **kwargs):
        return ChooseBarrierTypeForm()

    def get_context_data(self, *args, **kwargs):
        context = super(ReportCreateBarrierView, self).get_context_data(*args, **kwargs)
        # warning - this will need to change if we change
        # the code of the UK barrier source
        uk_source = BarrierSource.objects.get(short_name='UK')
        uk_barrier_types = BarrierType.objects.filter(barrier_source=uk_source)
        context['barrier_types'] = uk_barrier_types
        return context

class ReportCreateBarrierFilteredView(FormView):
    model = BarrierReport
    template_name = 'backend/report-create-barrier-filtered.html'

    def get_form(self, *args, **kwargs):
        return ChooseBarrierTypeForm(initial={'barrier_type': '93'})

    def get_context_data(self, *args, **kwargs):
        context = super(ReportCreateBarrierFilteredView, self).get_context_data(*args, **kwargs)
        # warning - this will need to change if we change
        # the code of the UK barrier source
        uk_source = BarrierSource.objects.get(short_name='UK')
        uk_barrier_types = BarrierType.objects.filter(barrier_source=uk_source)
        context['barrier_types'] = uk_barrier_types
        return context

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

class ReportAssignLeadView(FormView):
    model = BarrierReport
    template_name = 'backend/report-assign-lead.html'
    form_class = ChooseBarrierTypeForm

    def get_context_data(self, *args, **kwargs):
        context = super(ReportAssignLeadView, self).get_context_data(*args, **kwargs)
        # warning - this will need to change if we change
        # the code of the UK barrier source
        uk_source = BarrierSource.objects.get(short_name='UK')
        uk_barrier_types = BarrierType.objects.filter(barrier_source=uk_source)
        context['barrier_types'] = uk_barrier_types
        return context

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

# Assessment and resolutions
class BarrierSummaryView(ListView):
    model = BarrierReport
    template_name = 'backend/barrier-summary.html'
    pass

class BarrierSummaryResolutionView(ListView):
    model = BarrierReport
    template_name = 'backend/barrier-summary-resolution.html'
    pass

class BarrierOrganisationalImpactView(ListView):
    model = BarrierReport
    template_name = 'backend/barrier-organisational-impact.html'
    pass

class BarrierImpactOnTheUKView(ListView):
    model = BarrierReport
    template_name = 'backend/barrier-impact-on-the-uk.html'
    pass

class BarrierChanceOfSuccessView(ListView):
    model = BarrierReport
    template_name = 'backend/barrier-chance-of-success.html'
    pass

class BarrierAssociatedBarriersView(ListView):
    model = BarrierReport
    template_name = 'backend/barrier-associated-barriers.html'
    pass

class BarrierResolutionContextView(ListView):
    model = BarrierReport
    template_name = 'backend/barrier-resolution-context.html'
    pass

class BarrierInteractionsView(ListView):
    model = BarrierReport
    template_name = 'backend/barrier-interactions.html'
    pass

class BarrierEventsView(ListView):
    model = BarrierReport
    template_name = 'backend/barrier-events.html'
    pass

class BarrierContactsView(ListView):
    model = BarrierReport
    template_name = 'backend/barrier-contacts.html'
    pass

class BarrierInstancesView(ListView):
    model = BarrierReport
    template_name = 'backend/barrier-instances.html'
    pass

class BarrierSensitivitiesView(ListView):
    model = BarrierReport
    template_name = 'backend/barrier-sensitivities.html'
    pass

class BarrierPublicSummaryView(ListView):
    model = BarrierReport
    template_name = 'backend/barrier-public-summary.html'
    pass
