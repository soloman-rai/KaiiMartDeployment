from django.core.exceptions import ValidationError
import re


def phone_validation(phone_num):
    regex = '\d{10}'

    if not re.search(regex, phone_num):
        raise ValidationError('Phone number must be digits and no more than 10')    
    