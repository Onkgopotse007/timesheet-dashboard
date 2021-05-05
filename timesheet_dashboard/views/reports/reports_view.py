import datetime
import pandas as pd
from django.apps import apps as django_apps
from edc_base.utils import get_utcnow
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
        download = self.request.GET.get('download')

        # self.get_employees_by_month(5)
        if download == '1':
            self.get_all_timesheets_by_month(5)
        return context

    def get_employees_by_month(self, month):

        employees_cls = django_apps.get_model('bhp_personnel.employee')

        contracts_cls = django_apps.get_model('bhp_personnel.contract')

        contract_extensions_cls = django_apps.get_model('bhp_personnel.contractextension')

        active_contracts = contracts_cls.objects.filter(end_date__month__gte=month)

        active_employees = active_contracts.values_list('identifier', flat=True)

        employees = employees_cls.objects.filter(identifier__in=active_employees).values_list(
                'employee_code', flat=True)

        # data_dict =
        for employee in employees:
            pass

    def get_all_timesheets_by_month(self, month):

        daily_entry_cls = django_apps.get_model('timesheet.dailyentry')

        daily_entries = daily_entry_cls.objects.filter(
            day__month=month).values()

        daily_entries_df = pd.DataFrame(daily_entries)

        daily_entries_df.drop(['hostname_created', 'hostname_modified',
                               'revision', 'device_created', 'device_modified',
                               'id'], axis=1, inplace=True)

        monthly_entry_cls = django_apps.get_model('timesheet.monthlyentry')

        monthly_entries = monthly_entry_cls.objects.filter(
            month__month=month).values()

        monthly_entries_df = pd.DataFrame(monthly_entries)

        monthly_entries_df.drop(['hostname_created', 'hostname_modified',
                               'revision', 'device_created', 'device_modified',
                               'site_id', 'slug', 'created', 'user_created',
                               'modified', 'user_modified', ], axis=1, inplace=True)

        entries_merged_left = pd.merge(left=daily_entries_df, right=monthly_entries_df,
                                       how='left', left_on='monthly_entry_id', right_on='id')

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        fname = f'{month}_timesheets_{timestamp}.csv'
        final_path = '/Users/imosweu/Desktop/' + fname

        entries_merged_left.drop(['id', 'monthly_entry_id'], axis=1, inplace=True)

        entries_merged_left.to_csv(final_path, encoding='utf-8', index=False)

    # def get_all_timesheets_by_employee(self, employee_id, start_datetime, end_datetime):
    #
        # daily_entry_cls = django_apps.get_model('timesheet.dailyentry')
        #
        # daily_entries = daily_entry_cls.objects.filter(
            # day__month=month).values()
            #
        # monthly_entry_df = pd.DataFrame(daily_entries)
        #
        # monthly_entry_df.drop(['hostname_created', 'hostname_modified',
                 # 'revision', 'device_created', 'device_modified',
                 # 'id'], axis=1, inplace=True)

