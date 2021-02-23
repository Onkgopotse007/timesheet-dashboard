from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'timesheet_dashboard' else False

timesheet_dashboard = Navbar(name='timesheet_dashboard')

timesheet_dashboard.append_item(
    NavbarItem(
        name='employee_timesheet',
        label='Timesheets',
        fa_icon='fas fa-stopwatch',
        url_name=settings.DASHBOARD_URL_NAMES.get('timesheet_home_url'),
        no_url_namespace=no_url_namespace))

site_navbars.register(timesheet_dashboard)
