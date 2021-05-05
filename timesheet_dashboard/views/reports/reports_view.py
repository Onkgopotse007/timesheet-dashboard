import pandas as pd
from django.apps import apps as django_apps
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin


class ReportsView(EdcBaseViewMixin, NavbarViewMixin, BaseDashboardView):

    dashboard_url = 'reports_dashboard_url'
    dashboard_template = 'reports_dashboard_template'
    navbar_name = 'timesheet'
    navbar_selected_item = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.get_all_timesheets_by_month(5)
        return context

    def get_all_timesheets_by_month(self, month):

        daily_entry_cls = django_apps.get_model('timesheet.dailyentry')

        daily_entries = daily_entry_cls.objects.filter(
            day__month=month).values()

        monthly_entry_df = pd.DataFrame(daily_entries)

        monthly_entry_df.drop(['hostname_created', 'hostname_modified',
                 'revision', 'device_created', 'device_modified',
                 'id', 'site_id', 'slug'], axis=1, inplace=True)

        import pdb; pdb.set_trace()

        print(monthly_entry_df)

