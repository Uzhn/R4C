from django.conf import settings
from django.core.mail import send_mail


def send_notification(email, model, version):
    """Функция отправки письма на почту пользователю, о наличии робота, которого он заказывал."""
    message = (f'Добрый день!\nНедавно вы интересовались нашим роботом модели {model}, '
               f'версии {version}.\nЭтот робот теперь в наличии. '
               f'Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.')
    send_mail(
        'Робот доступен в наличии',
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
