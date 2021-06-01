from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .monthly_entry_model_wrapper import MonthlyEntryModelWrapper


class MonthlyEntryModelWrapperMixin:

    monthly_entry_model_wrapper_cls = MonthlyEntryModelWrapper

