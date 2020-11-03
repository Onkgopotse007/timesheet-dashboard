from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'timesheet_dashboard' else False

timesheet_dashboard = Navbar(name='timesheet_dashboard')

timesheet_dashboard.append_item(
    NavbarItem(
        name='employee_timesheet',
        label='My Timesheets',
        fa_icon='fa-clock-o',
        url_name=settings.DASHBOARD_URL_NAMES.get('timesheet_listboard_url'),
        no_url_namespace=no_url_namespace))

site_navbars.register(timesheet_dashboard)
