from django.conf import settings
from edc_model_wrapper import ModelWrapper
from django.apps import apps as django_apps


class MonthlyEntryModelWrapper(ModelWrapper):

    model = 'timesheet.monthlyentry'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'timesheet_listboard_url')
    next_url_attrs = ['employee']
    querystring_attrs = ['employee', 'month']


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
        except self.monthly_entry_cls.ObjectDoesNotExist:
            return None

    @property
    def monthly_entry(self):
        """Returns a wrapped saved or unsaved monthly entry.
        """
        import pdb; pdb.set_trace()
        model_obj = self.monthly_entry_model_obj or self.monthly_entry_cls(
            **self.monthly_entry_options)
        return self(model_obj=model_obj)

    @property
    def monthly_entry_cls(self):
        return django_apps.get_model('potlako_subject.monthlyentry')

    @property
    def monthly_entry_options(self):
        """Returns a dictionary of options to get an existing
        verbal consent model instance.
        """
        options = dict(
            employee_id=self.employee.id)
        return options

    @property
    def employee(self):
        employee_cls = django_apps.get_model('bhp_personnel.employee')
        try:
            employee_obj = employee_cls.objects.get(email=self.request.user.email)
        except employee_cls.DoesNotExist:
            employee_obj = None
        return employee_obj




