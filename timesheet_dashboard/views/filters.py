# from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters
#
#
# class ListboardViewFilters(ListboardViewFilters):
#
#     all = ListboardFilter(
#         name='all',
#         label='All',
#         lookup={})
#
#     eligible = ListboardFilter(
#         label='year',
#         position=10,
#         lookup={'is_eligible': True})
#
#     not_eligible = ListboardFilter(
#         label='Not Eligible',
#         position=11,
#         lookup={'is_eligible': False})
#
#     consented = ListboardFilter(
#         label='Consented',
#         position=20,
#         lookup={'is_eligible': True,
#                 'is_consented': True})
#
#     not_consented = ListboardFilter(
#         label='Not consented',
#         position=21,
#         lookup={'is_eligible': True,
#                 'is_consented': False})
