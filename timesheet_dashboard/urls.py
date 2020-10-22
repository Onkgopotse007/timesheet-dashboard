from django.urls import path
from edc_dashboard import UrlConfig

from .patterns import order_number
from .views import (HomeView, PurchaseOrderListboardView, )

app_name = 'timesheet_dashboard'

timesheet_listboard_url_config = UrlConfig(
    url_name='timesheet_listboard_url',
    view_class=PurchaseOrderListboardView,
    label='timesheet_listboard',
    identifier_label='order_number',
    identifier_pattern=order_number)


urlpatterns = []
urlpatterns += [path('listboard/', HomeView.as_view(), name='procurement_url')]
urlpatterns += purchase_order_listboard_url_config.listboard_urls
urlpatterns += purchase_order_report_url_config.listboard_urls
