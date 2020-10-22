from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'timesheet_dashboard' else False

timesheet_listboard = Navbar(name='timesheet_listboard')

timesheet_listboard.append_item(
    NavbarItem(
        name='employee_timesheet',
        title='Employee Timesheet',
        label='Employee Timesheet',
        fa_icon='fa fa-clock',
        url_name=settings.DASHBOARD_URL_NAMES[
            'timesheet_listboard_url'],
        no_url_namespace=no_url_namespace))

site_navbars.register(timesheet_listboard)
