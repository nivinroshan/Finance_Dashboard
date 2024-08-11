from django import template

register = template.Library()

@register.filter
def badge_class(transaction_type):
    return 'success' if transaction_type == 'income' else 'danger'
