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
