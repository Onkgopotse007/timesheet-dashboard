from django.apps import AppConfig as DjangoAppConfig
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig


class AppConfig(DjangoAppConfig):
    name = 'timesheet_dashboard'
    admin_site_name = 'timesheet_admin'


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'Timesheet Dashboard'
    institution = 'Botswana Harvard'
    disclaimer = 'Employee Timesheet'
