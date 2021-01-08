from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters


class ListboardViewFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    new = ListboardFilter(
        label='New',
        position=10,
        lookup={'status': 'new'})

    approved = ListboardFilter(
        label='Approved',
        position=11,
        lookup={'status': 'approved'})

    verified = ListboardFilter(
        label='Verified',
        position=20,
        lookup={'status': 'verified'})

    rejected = ListboardFilter(
        label='Rejected',
        position=21,
        lookup={'status': 'rejecetd'})
