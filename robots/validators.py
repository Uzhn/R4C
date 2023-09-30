from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_created(value):
    """Проверка даты создания не больше текущей."""
    if value > timezone.now():
        raise ValidationError('The creation date cannot be greater than the current date.')
