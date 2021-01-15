from django import template
from django.apps import apps as django_apps
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
def timesheets_button(model_wrapper, p_role, user):
    title = ['View Employee Timesheets.']
    return dict(
        employee_id=model_wrapper.object.identifier,
        href=model_wrapper.href,
        timesheet_listboard_url=settings.DASHBOARD_URL_NAMES.get('timesheet_listboard_url'),
        groups=[g.name for g in user.groups.all()],
        p_role=p_role,
        title=' '.join(title))


@register.simple_tag(takes_context=True)
def departments(context):
    department_cls = django_apps.get_model('bhp_personnel.department')

    return [dept.dept_name for dept in department_cls.objects.all()]

