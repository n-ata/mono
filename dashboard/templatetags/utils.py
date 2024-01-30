from django import template
from django.urls import translate_url, reverse
from datetime import datetime, date
import pytz

register = template.Library()
format_data = "%Y-%m-%d"

@register.filter(name='has_group') 
def has_group(user, group_name):
    if (user.groups.filter(name=group_name).exists() and user.is_staff) or user.is_superuser:
        return True
    return False

@register.simple_tag(takes_context=True)
def sub_menu_link_active(context, url_to_check: str) -> str:
    request = context['request']
    if request.get_full_path() == reverse(url_to_check):
        return "active"
    return ""

@register.simple_tag(takes_context=True)
def menu_link_active(context, url_to_check: str) -> str:
    request = context['request']
    splitted_path = request.get_full_path().split('/')
    full_path = splitted_path[1] + '/' + splitted_path[2]
    if full_path in reverse(url_to_check):
        return "hover show"
    return ""

@register.simple_tag(takes_context=True)
def convert_date(context, dat: str) -> str:
    if dat:
        return dat
    return date.today().strftime(format_data)