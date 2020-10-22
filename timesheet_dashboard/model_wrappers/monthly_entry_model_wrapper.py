from django.conf import settings
from edc_model_wrapper import ModelWrapper


class MonthlyEntryModelWrapper(ModelWrapper):

    model = 'timesheet.monthlyentry'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'timesheet_listboard_url')
    next_url_attrs = ['employee_identifier']
    querystring_attrs = ['employee_identifier', ]
    
    
    @property
    def employee_identifier(self):
        return self.object.employee.identifier
