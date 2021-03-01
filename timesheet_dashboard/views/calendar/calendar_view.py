import calendar
import math
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
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
from smtplib import SMTPException


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
    daily_entry_cls = django_apps.get_model('timesheet.dailyentry')

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
            elif request.POST.get('read_only') == '1' or request.POST.get('timesheet_review'):
                self.add_daily_entries(request, kwargs)
                return HttpResponseRedirect(reverse('timesheet_dashboard:timesheet_listboard_url', 
                                            kwargs={'employee_id': kwargs.get('employee_id')})
                                            +'?p_role='+request.GET.get('p_role'))
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

    def clean_data(self, data, daily_entries_count):

        for i in range(daily_entries_count):
            index = str(i+1)
            day = data.get(index+'-day')
            day_date = datetime.strptime(day, '%Y-%m-%d')
            try:
                daily_entry_obj = self.daily_entry_cls.objects.get(day=day_date)
            except self.daily_entry_cls.DoesNotExist:
                pass
            else:
                duration = int(data.get(index + '-duration'))
                entry_type = data.get(index + '-entry_type')
                if (daily_entry_obj.duration != duration
                        or daily_entry_obj.entry_type != entry_type):

                    daily_entry_obj.duration = duration
                    daily_entry_obj.entry_type = entry_type
                    daily_entry_obj.save()
                data.pop(index + '-duration')
                data.pop(index + '-entry_type')
                data.pop(index + '-row')
                data.pop(index + '-day')

    def add_daily_entries(self, request, *args, **kwargs):
        monthly_entry_cls = django_apps.get_model(self.model)
        data = request.POST.dict()
        year = self.kwargs.get('year', '')
        month = self.kwargs.get('month', '')
        daily_entries = None

        if request.POST.get('timesheet_review'):
            try:
                monthly_entry = monthly_entry_cls.objects.get(
                    employee=self.get_employee, supervisor=self.get_employee.supervisor,
                    month=datetime.strptime(f'{year}-{month}-1', '%Y-%m-%d'))
            except monthly_entry_cls.DoesNotExist:
                pass  # raise exception
            else:
                if request.POST.get('comment'):
                    monthly_entry.comment = request.POST.get('comment')
                monthly_entry.status = request.POST.get('timesheet_review')
                monthly_entry.save()
                
                if request.POST.get('timesheet_review') in ['rejected', 'verified']:
                    
                    subject = f'Timesheet for {monthly_entry.month}'
                    message = (f'Dear {monthly_entry.employee.first_name}, Your timesheet '
                               f'for {monthly_entry.month} has been {monthly_entry.status}.')
                    if request.POST.get('comment'):
                        comment_msg = ' Comment: '+request.POST.get('comment')
                        message += comment_msg
                    from_email = settings.EMAIL_HOST_USER
                    user = monthly_entry.employee.email
                    try:
                        send_mail(subject, message, from_email, [user, ], fail_silently=False)
                    except SMTPException as e:
                        raise ValidationError(
                            f'There was an error sending an email: {e}')
        else:
            try:
                monthly_entry = monthly_entry_cls.objects.get(
                    employee=self.get_employee, supervisor=self.get_employee.supervisor,
                    month=datetime.strptime(f'{year}-{month}-1', '%Y-%m-%d'))
            except monthly_entry_cls.DoesNotExist:
                monthly_entry = monthly_entry_cls(employee=self.get_employee or None,
                                                  supervisor=self.get_employee.supervisor,
                                                  month=datetime.strptime(f'{year}-{month}-1', '%Y-%m-%d'))
            else:
                daily_entries = self.daily_entry_cls.objects.filter(monthly_entry=monthly_entry)

            DailyEntryFormSet = inlineformset_factory(monthly_entry_cls,
                                                      self.daily_entry_cls,
                                                      form=DailyEntryForm,
                                                      fields=['day', 'duration', 'entry_type', 'row'],
                                                      can_delete=True)

            if daily_entries:
                self.clean_data(data, daily_entries.count())

            total_forms = int(data.get('dailyentry_set-TOTAL_FORMS'))

            for i in range(total_forms):
                index = str(i)

                day = data.get('dailyentry_set-' + index + '-day')
                day = f'{year}-{month}-' + str(day)
                day_date = datetime.strptime(day, '%Y-%m-%d')
                data['dailyentry_set-' + index + '-day'] = day_date

            formset = DailyEntryFormSet(data=data, instance=monthly_entry)  #, initial=daily_entries.__dict__)

            if formset.is_valid():
                if request.POST.get('save_submit') == '1':
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

        monthly_obj = self.get_monthly_obj(datetime.strptime(f'{year}-{month}-1', '%Y-%m-%d'))
        extra_context = {}
        if (self.request.GET.get('p_role') == 'Supervisor'):
            extra_context = {'review': True,
                             'p_role': 'Supervisor'}
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
                       entry_types=self.entry_types(),
                       et=['RH',  'RL', 'SL', 'H', 'ML', 'PL', 'CL', 'STL'],
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

    def get_number_of_weeks(self, year, month):
        return len(calendar.monthcalendar(year,month))

    def get_weekdays(self, currDate=None):
        dates = [(currDate + timedelta(days=i)) for i in range(0 - currDate.weekday(), 7 - currDate.weekday())]
        return dates

    def get_dailyentries(self, year, month):
        monthly_entry_cls = django_apps.get_model('timesheet.monthlyentry')
        entries_dict = {}
        try:
            monthly_entry_obj = monthly_entry_cls.objects.get(
                        employee=self.get_employee,
                        month=datetime.strptime(f'{year}-{month}-1', '%Y-%m-%d'))
        except monthly_entry_cls.DoesNotExist:
            return None
        else:
            daily_entries = monthly_entry_obj.dailyentry_set.all()

            if daily_entries:
                daily_entries = daily_entries.order_by('day')
                rows = math.ceil(daily_entries.count()/7)

                entries_dict = {}
                for i in range(rows):
                    entries_dict[i] = list(daily_entries.filter(row=i))
        return entries_dict

    def get_blank_days(self, year, month):
        calendar_days = self.calendar_obj.monthdayscalendar(year, month)

        blank_days = 0

        for i in calendar_days[0]:
            if i == 0:
                blank_days += 1
        return blank_days

    @property
    def get_employee(self):
        employee_cls = django_apps.get_model('bhp_personnel.employee')

        try:
            employee_obj = employee_cls.objects.get(identifier=self.kwargs.get('employee_id'))
        except employee_cls.DoesNotExist:
            return None
        return employee_obj

    @property
    def user(self):
        employee_cls = django_apps.get_model('bhp_personnel.employee')

        try:
            employee_obj = employee_cls.objects.get(email=self.request.user.email)
        except employee_cls.DoesNotExist:
            return None
        return employee_obj


    def entry_types(self):
        daily_entry_cls = django_apps.get_model('timesheet.dailyentry')
        return daily_entry_cls._meta.get_field('entry_type').choices
