from edc_dashboard import UrlConfig
from django.contrib.auth import get_user_model
from .patterns import identifier
from .views import ListboardView, EmployeeListBoardView, CalendarView, ReportsView
from .calendar_url_config import UrlConfig as CalendarUrlConfig

app_name = 'timesheet_dashboard'

User = get_user_model()

timesheet_listboard_url_config = UrlConfig(
    url_name='timesheet_listboard_url',
    view_class=ListboardView,
    label='timesheet_listboard',
    identifier_label='employee_id',
    identifier_pattern=identifier)

timesheet_employee_listboard_url_config = UrlConfig(
    url_name='timesheet_employee_listboard_url',
    view_class=EmployeeListBoardView,
    label='employee_timesheet_listboard',
    identifier_label='employee_id',
    identifier_pattern=identifier)

timesheet_calendar_url_config = CalendarUrlConfig(
    url_name='timesheet_calendar_table_url',
    view_class=CalendarView,
    label='timesheet_calendar_table',
    identifier_label='employee_id',
    identifier_pattern=identifier)

reports_dashboard_url_config = UrlConfig(
    url_name='reports_dashboard_url',
    view_class=ReportsView,
    label='reports_dashboard',
    identifier_label='reports',
    identifier_pattern='/')

urlpatterns = []
urlpatterns += timesheet_listboard_url_config.listboard_urls
urlpatterns += timesheet_employee_listboard_url_config.listboard_urls
urlpatterns += timesheet_calendar_url_config.calendar_urls
urlpatterns += reports_dashboard_url_config.listboard_urls
