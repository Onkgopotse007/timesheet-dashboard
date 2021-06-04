import calendar
import math
from datetime import datetime, timedelta
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Sum, Q
from django.forms import inlineformset_factory
from edc_base.utils import get_utcnow
from timesheet.forms import DailyEntryForm
from smtplib import SMTPException


class MonthlyEntryError(Exception):
    pass


class TimesheetMixin:

    def navigate_table(self, controller, year, month):
        if controller == 'next':
            if month == '12':
                year = int(year) + 1
                month = 1
            else:
                month = int(month) + 1
        elif controller == 'prev':
            if month == '1':
                year = int(year) - 1
                month = 12
            else:
                month = int(month) - 1

        return year, month

    def clean_data(self, data, daily_entries_count, monthly_entry):
        """ Remove duplicate entries from the formset data """
        for i in range(daily_entries_count):
            index = str(i + 1)
            day = data.get(index + '-day')

            day_date = datetime.strptime(day, '%Y-%m-%d')
            try:
                daily_entry_obj = self.daily_entry_cls.objects.get(day=day_date,
                                                                   monthly_entry=monthly_entry)
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
                    employee=self.employee, supervisor=self.employee.supervisor,
                    month=datetime.strptime(f'{year}-{month}-1', '%Y-%m-%d'))
            except monthly_entry_cls.DoesNotExist:
                raise MonthlyEntryError(f"Missing timesheet being reviewed for {self.employee}",
                                        f" for month starting {monthly_entry.month}.")
            else:
                if request.POST.get('comment').strip() != '':
                    monthly_entry.comment = request.POST.get('comment')
                else:
                    monthly_entry.comment = None
                prev_status = monthly_entry.status
                monthly_entry.status = request.POST.get('timesheet_review')

                if (prev_status != request.POST.get('timesheet_review')
                        and request.POST.get('timesheet_review') in
                        ['rejected', 'verified', 'approved']):
                    field_prefix = request.POST.get('timesheet_review')
                    setattr(monthly_entry, (field_prefix + '_date'), get_utcnow().date())
                    setattr(monthly_entry, (field_prefix + '_by'), (
                        request.user.first_name[0] + ' ' + request.user.last_name))
                    if request.POST.get('timesheet_review') == 'rejected':
                        setattr(monthly_entry, ('verified_date'), None)
                        setattr(monthly_entry, ('verified_by'), None)
                        setattr(monthly_entry, ('approved_date'), None)
                        setattr(monthly_entry, ('approved_by'), None)

                    current_site = get_current_site(request=None)

                    subject = f'Timesheet for {monthly_entry.month}'
                    message = (f'Dear {monthly_entry.employee.first_name},\n\nPlease note '
                               f'your timesheet for {monthly_entry.month} has been '
                               f'{monthly_entry.status} by {request.user.first_name} '
                               f'{request.user.last_name} on the BHP Utility system '
                               f'http://{current_site.domain}. \n\n')
                    if request.POST.get('comment').strip() != '':
                        comment_msg = 'Comment: ' + request.POST.get('comment') + '\n\n'
                        message += comment_msg
                    message += 'Good day :).'
                    from_email = settings.EMAIL_HOST_USER
                    user = monthly_entry.employee.email
                    try:
                        send_mail(subject, message, from_email, [user, ], fail_silently=False)
                    except SMTPException as e:
                        raise ValidationError(
                            f'There was an error sending an email: {e}')
                monthly_entry.save()
        else:
            try:
                monthly_entry = monthly_entry_cls.objects.get(
                    employee=self.employee, supervisor=self.employee.supervisor,
                    month=datetime.strptime(f'{year}-{month}-1', '%Y-%m-%d'))
            except monthly_entry_cls.DoesNotExist:
                monthly_entry = monthly_entry_cls(employee=self.employee,
                                                  supervisor=self.employee.supervisor,
                                                  month=datetime.strptime(
                                                      f'{year}-{month}-1', '%Y-%m-%d'))
            else:
                daily_entries = self.daily_entry_cls.objects.filter(
                    monthly_entry=monthly_entry)
                monthly_entry.comment = None

            DailyEntryFormSet = inlineformset_factory(monthly_entry_cls,
                                                      self.daily_entry_cls,
                                                      form=DailyEntryForm,
                                                      fields=['day', 'duration',
                                                              'entry_type', 'row'],
                                                      can_delete=True)

            if daily_entries:
                self.clean_data(data, daily_entries.count(), monthly_entry)

            total_forms = int(data.get('dailyentry_set-TOTAL_FORMS'))
            for i in range(total_forms):
                index = str(i)
                day = data.get('dailyentry_set-' + index + '-day')
                day = f'{year}-{month}-' + str(day)
                day_date = datetime.strptime(day, '%Y-%m-%d')
                data['dailyentry_set-' + index + '-day'] = day_date

            formset = DailyEntryFormSet(data=data, instance=monthly_entry)

            if formset.is_valid():
                if request.POST.get('save_submit') == '1':
                    monthly_entry.status = 'submitted'
                    monthly_entry.submitted_datetime = get_utcnow()

                monthly_entry = self.sum_monthly_leave_days(formset.queryset, monthly_entry)
                monthly_entry = self.calculate_monthly_overtime(
                    formset.queryset, monthly_entry)
                monthly_entry.save()
                current_contract = self.get_current_contract(monthly_entry.employee_id)
                if current_contract:
                    current_contract.leave_balance = (current_contract.leave_balance -
                                                      monthly_entry.annual_leave_taken)
                formset.save()

    def sum_monthly_leave_days(self, dailyentries, monthly_entry):

        leave_types = ['AL', 'STL', 'SL', 'CL', 'ML', 'PL']
        leave_taken_types = ['annual_leave_taken', 'study_leave_taken', 'sick_leave_taken',
                             'compassionate_leave_taken', 'maternity_leave_taken',
                             'paternity_leave_taken']

        for leave_type, leave_taken in zip(leave_types, leave_taken_types):
            leave_entries = dailyentries.filter(entry_type=leave_type)
            leave_sum_dict = leave_entries.aggregate(Sum('duration'))
            if leave_sum_dict.get('duration__sum'):
                setattr(monthly_entry, leave_taken, leave_sum_dict.get('duration__sum') / 8)

        return monthly_entry

    def get_current_contract(self, employee_id):

        contract_cls = django_apps.get_model('bhp_personnel.contract')
        try:
            current_contract = contract_cls.objects.get(identifier=employee_id,
                                                        status='Active')
        except contract_cls.DoesNotExist:
            pass
        else:
            return current_contract

    def calculate_monthly_overtime(self, dailyentries, monthly_entry):

        weekday_entries = dailyentries.filter(Q(day__week_day__lt=7) & Q(day__week_day__gt=1),
                                              entry_type='RH')

        extra_hours = 0

        for entry in weekday_entries:
            if entry.duration > 8:
                extra_hours += entry.duration - 8

        overtime = extra_hours

        weekend_entries = dailyentries.filter(Q(entry_type='WE') | Q(entry_type='H'))

        weekend_entries_dict = weekend_entries.aggregate(Sum('duration'))

        if weekend_entries_dict.get('duration__sum'):
            overtime += weekend_entries_dict.get('duration__sum')

        monthly_entry.monthly_overtime = overtime

        return monthly_entry

    def get_holidays(self, year, month):
        facility_app_config = django_apps.get_app_config('edc_facility')

        facility = facility_app_config.get_facility('5-day clinic')

        holiday_list = facility.holidays.holidays.filter(
            local_date__year=year,
            local_date__month=month).values_list('local_date', flat=True)
        return '|'.join([f'{h.year}/{h.month}/{h.day}' for h in holiday_list])

    def get_monthly_obj(self, month):

        monthly_cls = django_apps.get_model('timesheet.monthlyentry')

        try:
            monthly_obj = monthly_cls.objects.get(month=month,
                                                  employee=self.employee,)
        except monthly_cls.DoesNotExist:
            monthly_obj = None
        return monthly_obj

    def get_number_of_weeks(self, year, month):
        return len(calendar.monthcalendar(year, month))

    def get_weekdays(self, currDate=None):
        dates = [(currDate + timedelta(days=i)) for i in range(
            0 - currDate.weekday(), 7 - currDate.weekday())]
        return dates

    def get_dailyentries(self, year, month):
        monthly_entry_cls = django_apps.get_model('timesheet.monthlyentry')
        entries_dict = {}
        try:
            monthly_entry_obj = monthly_entry_cls.objects.get(
                        employee=self.employee,
                        month=datetime.strptime(f'{year}-{month}-1', '%Y-%m-%d'))
        except monthly_entry_cls.DoesNotExist:
            return None
        else:
            daily_entries = monthly_entry_obj.dailyentry_set.all()
            blank_days = self.get_blank_days(int(year), int(month))

            if daily_entries:
                daily_entries = daily_entries.order_by('day')
                rows = math.ceil((daily_entries.count() + blank_days) / 7)
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
    def employee(self):
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
        entry_types = daily_entry_cls._meta.get_field('entry_type').choices
        entry_types = tuple(entry_type for entry_type in entry_types
                            if entry_type[0] not in ['H', 'WE'])
        return entry_types
