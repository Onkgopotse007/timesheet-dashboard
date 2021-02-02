from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters
from django.apps import apps as django_apps


class ListboardViewFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    new = ListboardFilter(
        label='New',
        position=1,
        lookup={'status': 'new'})

    submitted = ListboardFilter(
        label='Submitted',
        position=2,
        lookup={'status': 'submitted'})

    approved = ListboardFilter(
        label='Approved',
        position=3,
        lookup={'status': 'approved'})

    verified = ListboardFilter(
        label='Verified',
        position=4,
        lookup={'status': 'verified'})

    rejected = ListboardFilter(
        label='Rejected',
        position=5,
        lookup={'status': 'rejecetd'})


class EmployeeListboardViewFilters(ListboardViewFilters):

    def __init__(self, departments=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.departments:
            count = 1
            for dept in self.departments:
                ListboardFilter(
                label=dept,
                name=dept,
                position=count,
                lookup={'department__dept_name': dept})
            count = count + 1


    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    @property
    def departments(self):
        department_cls = django_apps.get_model('bhp_personnel.department')

        return [dept.dept_name for dept in department_cls.objects.all()]


