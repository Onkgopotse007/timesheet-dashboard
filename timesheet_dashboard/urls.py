from django.urls import path
from edc_dashboard import UrlConfig

from .views import ListboardView

app_name = 'timesheet_dashboard'

timesheet_listboard_url_config = UrlConfig(
    url_name='timesheet_listboard_url',
    view_class=ListboardView,
    label='timesheet_listboard',
    identifier_label='employee_identifier',
    identifier_pattern='')


urlpatterns = []
urlpatterns += timesheet_listboard_url_config.listboard_urls
