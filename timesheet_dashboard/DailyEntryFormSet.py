from django.core.exceptions import ValidationError
from django.forms import BaseFormSet
from django.forms import formset_factory
from timesheet.forms import DailyEntryForm


class BaseArticleFormSet(BaseFormSet):

    def clean(self):
        """Checks that no two articles have the same title."""
        if any(self.errors):
            raise ValidationError(self.errors)

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue

            duration = form.cleaned_data.get('duration')
