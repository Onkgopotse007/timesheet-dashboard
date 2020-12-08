import re
from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin
from django.contrib.auth import models

from ..model_wrappers import MonthlyEntryModelWrapper


class ListboardView(EdcBaseViewMixin, NavbarViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin,
                    ListboardView):
    listboard_template = 'timesheet_listboard_template'
    listboard_url = 'timesheet_listboard_url'
    listboard_panel_style = 'success'
    listboard_fa_icon = 'fa fa-list-alt'

    model = 'timesheet.monthlyentry'
    model_wrapper_cls = MonthlyEntryModelWrapper
    navbar_name = 'timesheet'
    navbar_selected_item = 'timesheet_listboard'
    search_form_url = 'timesheet_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            groups=[g.name for g in self.request.user.groups.all()],
            timesheet_add_url=self.model_cls().get_absolute_url())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        usr_groups = [g.name for g in self.request.user.groups.all()]
        if('HR' in usr_groups and request.GET.get('hr')):
            return options
        elif('Supervisor' in usr_groups and request.GET.get('email')):
            supervisor_cls = django_apps.get_model('bhp_personnel.supervisor')
            try:
                supervisor_obj = supervisor_cls.objects.get(email=request.GET.get('email'))
            except supervisor_cls.DoesNotExist:
                options.update({'user_created': None})
            else:
                options.update({'supervisor': supervisor_obj})
        else:
            options.update(
            {'user_created': request.user.username})
            
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
