from django import template

register = template.Library()

@register.inclusion_tag('timesheet_dashboard/buttons/submit_timesheet_button.html')
def submit_timesheet_button(model_wrapper):
    title = ['Submit Timesheet']
    return dict(
        employee_id=model_wrapper.object.employee.identifier,
        status=model_wrapper.object.status,
        month=model_wrapper.object.month,
        title=' '.join(title))

@register.inclusion_tag('timesheet_dashboard/buttons/view_timesheet_button.html')
def view_timesheet_button(model_wrapper):
    title = ['View Timesheet']
    return dict(
        employee_id=model_wrapper.object.employee.identifier,
        status=model_wrapper.object.status,
        month=model_wrapper.object.month,
        read_only=True,
        title=' '.join(title))
