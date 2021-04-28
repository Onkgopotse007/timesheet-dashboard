import calendar
import math
from datetime import datetime, timedelta
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
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
                monthly_entry.status = request.POST.get('timesheet_review')

                if request.POST.get('timesheet_review') in ['rejected', 'verified', 'approved']:
                    field_prefix = request.POST.get('timesheet_review')
                    setattr(monthly_entry, (field_prefix + '_date'), get_utcnow().date())
                    setattr(monthly_entry, (field_prefix + '_by'), (
                        request.user.first_name[0] + ' ' + request.user.last_name))

                    subject = f'Timesheet for {monthly_entry.month}'
                    message = (f'Dear {monthly_entry.employee.first_name}, Your timesheet '
                               f'for {monthly_entry.month} has been {monthly_entry.status} by'
                               f' {request.user.first_name} {request.user.last_name}.')
                    if request.POST.get('comment').strip() != '':
                        comment_msg = ' Comment: ' + request.POST.get('comment')
                        message += comment_msg
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
                monthly_entry.save()
                formset.save()

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
        return daily_entry_cls._meta.get_field('entry_type').choices
