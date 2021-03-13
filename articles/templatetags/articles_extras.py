from django import template

register = template.Library()


@register.filter()
def get_reading_time(value, step):
    if step not in ['sec', 'min']:
        raise ValueError('Invalid step')

    words_count = len(value.split(' '))
    reading_time_min = words_count / 120
    reading_time = reading_time_min if step == 'min' else reading_time_min * 60

    return f'{round(reading_time)} {step} to read'
