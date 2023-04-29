from datetime import datetime

def date_validator(data_text):
    try:
        datetime.strptime(data_text, '%d.%m.%Y')
    except ValueError:
        return False

    return True

def date_str_to_django(data_text):

    assert date_validator(data_text)
    d = datetime.strptime(data_text, '%d.%m.%Y')

    return d.strftime('%Y-%m-%d %H:%M')

def date_django_to_str(date):
    return date.strftime('%d-%m-%Y')
