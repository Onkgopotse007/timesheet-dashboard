from django.conf import settings
from edc_model_wrapper import ModelWrapper
from django.apps import apps as django_apps


class MonthlyEntryModelWrapper(ModelWrapper):

    model = 'timesheet.monthlyentry'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'timesheet_listboard_url')
    querystring_attrs = ['employee', 'year', 'month', 'supervisor']

    @property
    def employee(self):
        return self.object.employee

    @property
    def supervisor(self):
        return self.object.employee.supervisor

    @property
    def timesheet_status(self):
        return self.object.get_status_display()

    @property
    def monthly_entry_model_obj(self):
        """Returns a monthly entry model instance or None.
        """
        try:
            return self.monthly_entry_cls.objects.get(
                **self.monthly_entry_options)
        except self.monthly_entry_cls.DoesNotExist:
            return None

    @property
    def monthly_entry(self):
        """Returns a wrapped saved or unsaved monthly entry.
        """
        model_obj = self.monthly_entry_model_obj or self.monthly_entry_cls(
            **self.monthly_entry_options)
        return self(model_obj=model_obj)

    @property
    def month(self):
        if self.monthly_entry_model_obj:
            return self.monthly_entry_model_obj.month.month
        else:
            None

    @property
    def year(self):
        if self.monthly_entry_model_obj:
            return self.monthly_entry_model_obj.month.year
        else:
            None

    @property
    def monthly_entry_cls(self):
        return django_apps.get_model('timesheet.monthlyentry')

    @property
    def monthly_entry_options(self):
        """Returns a dictionary of options to get an existing
        monthly entry model instance.
        """
        options = dict(
            employee=self.object.employee,
            month=self.object.month)
        return options
