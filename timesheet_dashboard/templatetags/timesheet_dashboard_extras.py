from django import template

register = template.Library()

@register.inclusion_tag('timesheet_dashboard/buttons/submit_timesheet_button.html')
def submit_timesheet_button(model_wrapper):
    title = ['Submit Timesheet']
    return dict(
        employee_id=model_wrapper.object.employee.identifier,
        status=model_wrapper.object.status,
        title=' '.join(title))
