from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

ALPHABET = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz')


def match(text):
    return ALPHABET.isdisjoint(text.lower())


def validate_name(value):
    if match(value) or any(ch.isdigit() for ch in value):
        raise ValidationError(
            _("Имя и фамилия не могут содержать цифры или спецсимволы.")
        )
