from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
import datetime
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import TemplateRequestContextMixin
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from edc_navbar import NavbarViewMixin

from calendar import Calendar


class CalendarViewError(Exception):
    pass


class CalendarView(NavbarViewMixin, EdcBaseViewMixin,
                   TemplateRequestContextMixin, TemplateView):

    template_name = 'timesheet_dashboard/calendar/calendar_table.html'
    calendar_template = 'purchase_order_report_template'
    model = 'timesheet.monthlyentry'
    navbar_name = 'timesheet'
    navbar_selected_item = ''

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee_id = kwargs.get('employee_id', None)
        cal = Calendar()

        after_day = self.request.GET.get('day__gte', None)
        if not after_day:
            d = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = datetime.date.today()
        weeks = cal.monthdays2calendar(d.year, d.month)
        week_names = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

        datetime_object = datetime.datetime.strptime(str(d.month), "%m")
        month_name = datetime_object.strftime("%b")
        context.update(employee_id=employee_id,
                       month=month_name,
                       weeks=weeks,
                       week_name=week_names
                       )
        return context

    def filter_options(self, **kwargs):
        options = super().filter_options(**kwargs)
        if kwargs.get('employee_id'):
            options.update(
                {'employee_id': kwargs.get('employee_id')})
        return options

    @property
    def pdf_template(self):
        return self.get_template_from_context(self.calendar_template)
