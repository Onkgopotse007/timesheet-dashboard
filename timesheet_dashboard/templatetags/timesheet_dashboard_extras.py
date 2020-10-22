from django import template

register = template.Library()


@register.inclusion_tag('timesheet_dashboard/buttons/timesheet_button.html')
def timesheet_button(model_wrapper):
    title = ['Edit timesheet.']
    return dict(
        identifier=model_wrapper.object.employee_identifier,
        href=model_wrapper.href,
        title=' '.join(title))
