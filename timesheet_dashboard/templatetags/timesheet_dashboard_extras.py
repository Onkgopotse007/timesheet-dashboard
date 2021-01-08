from django import template
from django.conf import settings

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
        
@register.inclusion_tag('timesheet_dashboard/buttons/timesheets_button.html')
def timesheets_button(model_wrapper, user):
    title = ['View Employee Timesheets.']
    return dict(
        employee_id=model_wrapper.object.identifier,
        href=model_wrapper.href,
        timesheet_listboard_url=settings.DASHBOARD_URL_NAMES.get('timesheet_listboard_url'),
        groups=[g.name for g in user.groups.all()],
        title=' '.join(title))

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
