from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.urls.base import reverse
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import TemplateRequestContextMixin
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from edc_navbar import NavbarViewMixin
from timesheet.forms import MonthlyEntryForm, DailyEntryForm
from django.forms import inlineformset_factory

from calendar import Calendar
from django.shortcuts import redirect


class CalendarViewError(Exception):
    pass

class CalendarView(NavbarViewMixin, EdcBaseViewMixin,
                   TemplateRequestContextMixin, TemplateView):

    template_name = 'timesheet_dashboard/calendar/calendar_table.html'
    model = 'timesheet.monthlyentry'
    navbar_name = 'timesheet'
    navbar_selected_item = ''
    success_url = 'timesheet_dashboard:timesheet_calendar_table_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            self.add_daily_entries(request, kwargs)

        return HttpResponseRedirect(reverse(self.success_url, 
                                            kwargs={'employee_id': kwargs.get('employee_id'),
                                                    'year': kwargs.get('year'),
                                                    'month': kwargs.get('month'),
                                                    'day': kwargs.get('day')}))


    def add_daily_entries(self, request, *args, **kwargs):
        monthly_entry_cls = django_apps.get_model(self.model)

        daily_entry_cls = django_apps.get_model('timesheet.dailyentry')
        
        data = request.POST.dict()
        

        monthly_entry = monthly_entry_cls(employee=self.get_employee or None,
                                          supervisor=self.get_employee.supervisor,
                                          month=datetime.strptime(data.get('month'), '%Y-%m-%d'))

        DailyEntryFormSet = inlineformset_factory(monthly_entry_cls,
                                                  daily_entry_cls,
                                                  fields=('day', 'duration', 'entry_type'))
       
        for k in data:
            if '-day' in k:
                data[k] = datetime.strptime(data[k], '%Y-%m-%d')
                
        formset = DailyEntryFormSet(data=data, instance=monthly_entry)
        
        if formset.is_valid():
            monthly_entry.save()
            formset.save()
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee_id = kwargs.get('employee_id', None)
        year = kwargs.get('year', '')
        month = kwargs.get('month', '')
        day = kwargs.get('day', '')
        str_date = f'{year}/{month}/{day}'
        currDate = datetime.strptime(str_date, '%Y/%m/%d')
        start_date = None
#         curr_month = f'{year}/{month}/1'
        curr_month = datetime.strptime(f'{year}/{month}/1', '%Y/%m/%d')

        if self.request.GET.get('prev'):
            start_date = currDate - timedelta(weeks=1)
        elif self.request.GET.get('next'):
            start_date = currDate + timedelta(weeks=1)
        else:
            start_date = currDate
        if start_date:
            weeks = self.get_weekdays(start_date)

        context.update(employee_id=employee_id,
                       weeks=weeks,
                       curr_month=curr_month,
                       currDate=str_date)
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

    def get_weekdays(self, currDate=None):
        dates = [(currDate + timedelta(days=i)) for i in range(0 - currDate.weekday(), 7 - currDate.weekday())]
        return dates
    
    @property
    def get_employee(self):
        employee_cls = django_apps.get_model('bhp_personnel.employee')
        
        try:
            employee_obj = employee_cls.objects.get(identifier=self.kwargs.get('employee_id'))
        except employee_cls.DoesNotExist:
            return None
        return employee_obj

