from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    return dictionary.get(key)

@register.filter
def dictsort_by_date(attendances):
    return sorted(attendances, key=lambda attendance: attendance.date)