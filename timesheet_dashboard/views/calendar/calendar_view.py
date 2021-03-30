import calendar
from datetime import datetime
from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.urls.base import reverse
from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import TemplateRequestContextMixin
from edc_navbar import NavbarViewMixin
from .timesheet_mixin import TimesheetMixin


class CalendarViewError(Exception):
    pass


class CalendarView(TimesheetMixin, NavbarViewMixin, EdcBaseViewMixin,
                   TemplateRequestContextMixin, TemplateView):

    template_name = 'timesheet_dashboard/calendar/calendar_table.html'
    model = 'timesheet.monthlyentry'
    navbar_name = 'timesheet'
    navbar_selected_item = ''
    success_url = 'timesheet_dashboard:timesheet_calendar_table_url'
    calendar_obj = calendar.Calendar(firstweekday=0)
    daily_entry_cls = django_apps.get_model('timesheet.dailyentry')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # if this is a POST request we need to process the form data
        year = kwargs.get('year')
        month = kwargs.get('month')

        if request.method == 'POST':
            controller = request.POST.get('controller', '')
            if controller:
                year, month = self.navigate_table(controller, year, month)
            elif request.POST.get('read_only') == '1' or request.POST.get('timesheet_review'):
                self.add_daily_entries(request, kwargs)
                return HttpResponseRedirect(
                    reverse('timesheet_dashboard:timesheet_listboard_url',
                            kwargs={'employee_id': kwargs.get('employee_id')})
                            +'?p_role=' + request.GET.get('p_role'))
            else:
                self.add_daily_entries(request, kwargs)

        return HttpResponseRedirect(reverse('timesheet_dashboard:timesheet_calendar_table_url',
                                            kwargs={'employee_id': kwargs.get('employee_id'),
                                                    'year': year,
                                                    'month': month}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        employee_id = kwargs.get('employee_id', None)
        year = kwargs.get('year', '')
        month = kwargs.get('month', '')

        monthly_obj = self.get_monthly_obj(datetime.strptime(f'{year}-{month}-1', '%Y-%m-%d'))
        extra_context = {}
        if (self.request.GET.get('p_role') == 'Supervisor'):
            extra_context = {'p_role': 'Supervisor',
                             'verified': True,
                             'read_only': True,
                             'timesheet_status': monthly_obj.get_status_display()}
            if ((monthly_obj and monthly_obj.status != 'verified') or not monthly_obj):
                extra_context['review'] = True
        elif (self.request.GET.get('p_role') == 'HR'):
            extra_context = {'verify': True,
                             'p_role': 'HR'}
        elif (monthly_obj and monthly_obj.status in ['approved', 'verified']):
            extra_context = {'read_only': True,
                             'timesheet_status': monthly_obj.get_status_display()}

        month_name = calendar.month_name[int(month)]
        daily_entries_dict = self.get_dailyentries(int(year), int(month))
        blank_days = self.get_blank_days(int(year), int(month))
        no_of_weeks = self.get_number_of_weeks(int(year), int(month))
        groups = [g.name for g in self.request.user.groups.all()]

        entry_types = self.entry_types()

        if datetime.strptime(f'{year}-{month}-' + str(get_utcnow().day), '%Y-%m-%d'
                             ).date() > get_utcnow().date():
            entry_types = tuple(
                x for x in entry_types if x[0] not in ['RH', 'SL', 'CL', 'FH', ])

        context.update(employee_id=employee_id,
                       week_titles=calendar.day_abbr,
                       month_name=month_name,
                       curr_month=month,
                       year=year,
                       daily_entries_dict=daily_entries_dict,
                       prefilled_rows=len(daily_entries_dict.keys()) if daily_entries_dict else 0,
                       blank_days_range=range(blank_days),
                       blank_days=str(blank_days),
                       last_day=calendar.monthrange(int(year), int(month))[1],
                       no_of_weeks=no_of_weeks,
                       groups=groups,
                       user=self.user,
                       entry_types=entry_types,
                       comment=monthly_obj.comment if monthly_obj else None,
                       **extra_context)
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
