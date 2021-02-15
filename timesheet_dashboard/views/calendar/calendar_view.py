import calendar
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
from edc_base.utils import get_utcnow
from edc_dashboard.view_mixins import TemplateRequestContextMixin
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from edc_navbar import NavbarViewMixin
from timesheet.forms import MonthlyEntryForm, DailyEntryForm
from django.forms import inlineformset_factory
from django.forms import formset_factory


class CalendarViewError(Exception):
    pass


class CalendarView(NavbarViewMixin, EdcBaseViewMixin,
                   TemplateRequestContextMixin, TemplateView):

    template_name = 'timesheet_dashboard/calendar/calendar_table.html'
    model = 'timesheet.monthlyentry'
    navbar_name = 'timesheet'
    navbar_selected_item = ''
    success_url = 'timesheet_dashboard:timesheet_calendar_table_url'
    calendar_obj = calendar.Calendar(firstweekday=0)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

#     def get_success_url(self, **kwargs):
#         return HttpResponseRedirect(reverse('timesheet_dashboard:timesheet_calendar_table_url', 
#                                             kwargs={'employee_id': kwargs.get('employee_id'),
#                                                     'year': kwargs.get('year'),
#                                                     'month': kwargs.get('month'),
#                                                     'day': kwargs.get('day')}))

    def post(self, request, *args, **kwargs):
        # if this is a POST request we need to process the form data
        year = kwargs.get('year')
        month = kwargs.get('month')

        if request.method == 'POST':
            controller = request.POST.get('controller', '')
            if controller:
                year, month = self.navigate_table(controller, year, month)
            else:
                self.add_daily_entries(request, kwargs)

        return HttpResponseRedirect(reverse('timesheet_dashboard:timesheet_calendar_table_url', 
                                            kwargs={'employee_id': kwargs.get('employee_id'),
                                                    'year': year,
                                                    'month': month}))

    def navigate_table(self, controller, year, month):
        if controller == 'next' and month != '12':
            month = int(month) + 1
        elif controller == 'prev' and month != '1':
            month = int(month) - 1

        return year, month

    def clean_data(self, data):

        for i in range(0, 31):
            if 'dailyentry_set-'+str(i)+'-duration' in data.keys():
                if not data.get('dailyentry_set-' + str(i) + '-duration'):
                    data.pop('dailyentry_set-' + str(i) + '-duration')
                    data.pop('dailyentry_set-' + str(i) + '-entry_type')
                    data.pop('dailyentry_set-' + str(i) + '-day')
                    data['dailyentry_set-TOTAL_FORMS'] = int(data.get('dailyentry_set-TOTAL_FORMS'))-1
        return data

    def add_daily_entries(self, request, *args, **kwargs):
        monthly_entry_cls = django_apps.get_model(self.model)

        daily_entry_cls = django_apps.get_model('timesheet.dailyentry')

        data = request.POST.dict()
        year = self.kwargs.get('year', '')
        month = self.kwargs.get('month', '')
        
        monthly_entry = monthly_entry_cls(employee=self.get_employee or None,
                                          supervisor=self.get_employee.supervisor,
                                          month=datetime.strptime(f'{year}-{month}-1', '%Y-%m-%d'))

        DailyEntryFormSet = inlineformset_factory(monthly_entry_cls,
                                                  daily_entry_cls,
                                                  form=DailyEntryForm,
                                                  fields=['day', 'duration', 'entry_type'],
                                                  can_delete=True)

        for k in data:
            if '-day' in k:
                data[k] = datetime.strptime(data[k], '%Y-%m-%d')
        data = self.clean_data(data)

        formset = DailyEntryFormSet(data=data, instance=monthly_entry)
        if formset.is_valid():
            monthly_entry.status = 'submitted'
            monthly_entry.save()
            formset.save()

    def get_monthly_obj(self, month):

        monthly_cls = django_apps.get_model('timesheet.monthlyentry')

        try:
            monthly_obj = monthly_cls.objects.get(month=month)
        except monthly_cls.DoesNotExist:
            monthly_obj = None
        return monthly_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        employee_id = kwargs.get('employee_id', None)
        year = kwargs.get('year', '')
        month = kwargs.get('month', '')

        count=0
#         if self.get_monthly_obj(curr_month):
#             count = len(self.get_monthly_obj(curr_month).dailyentry_set.all())
        
        extra_context = {}   
        if (self.request.GET.get('p_role') == 'Supervisor'):
            extra_context = {'review': True}
        if (self.request.GET.get('p_role')=='HR'):
            extra_context = {'verify': True}
            
        month_name=calendar.month_name[int(month)]
        
        context.update(employee_id=employee_id,
                       week_titles=calendar.day_abbr,
                       month_name = month_name,
                       curr_month=month,
                       year = year,
#                        calender_days = self.get_calender_days(year, month),
#                        blank_days = blank_days,
                       no_of_weeks=self.get_number_of_weeks(int(year), int(month)),
                       count=count,
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
    
#     def get_calender_days(self, year, month):
#    
#         calendar_days = self.calendar_obj.monthdayscalendar(year, int(month))
#         
#         
#         blank_days = 0
#         
#         for i in calendar_days[0]:
#             if i==0:
#                 blank_days += 1
#                 
#         formatted_calendar_days = []
#         for week in calendar_days:
#             formatted_calendar_days
#         return blank_days, calendar_days
    
    def get_number_of_weeks(self, year, month):
        return len(calendar.monthcalendar(year,month))

    def get_weekdays(self, currDate=None):
        dates = [(currDate + timedelta(days=i)) for i in range(0 - currDate.weekday(), 7 - currDate.weekday())]
        return dates
    
    def get_dailyentries(self, year, month):
        daily_entry_cls = django_apps.get_model('timesheet.dailyentry')
        daily_entry_cls.objects.filter(day__year=year, day__month=month, entry_type='reg_hours').order_by('day')
        
#         self.get_calender_days(year, month)
        
        calendar_days = self.calendar_obj.monthdayscalendar(year, month)
        import pdb; pdb.set_trace()
        
#         blank_days = 0
#         
#         for i in calendar_days[0]:
#             if i==0:
#                 blank_days += 1
#                 
#         formatted_calendar_days = []
#         for week in calendar_days:
#             
#         for day in blank_days:
#             
#             formatted_calendar_days.append([0,0,0])
    

    @property
    def get_employee(self):
        employee_cls = django_apps.get_model('bhp_personnel.employee')

        try:
            employee_obj = employee_cls.objects.get(identifier=self.kwargs.get('employee_id'))
        except employee_cls.DoesNotExist:
            return None
        return employee_obj

#     def get_dailyentries(self, weeks):
#         daily_entry_cls = django_apps.get_model('timesheet.dailyentry')
#         hours = []
#         for day in weeks:
#             entries = daily_entry_cls.objects.filter(day=day, entry_type='reg_hours')
#             if entries:
#                 hours.append(entries[0].duration)
#             else:
#                 continue
#         return hours
