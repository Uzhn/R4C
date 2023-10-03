from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from services.notification import send_notification

from .models import Robot


@receiver(post_save, sender=Robot)
def notify_waiting_orders(sender, instance, **kwargs):
    """Сигнал оповещения пользователей, при добавлении робота."""
    waiting_orders = Order.objects.filter(robot_serial=instance.serial, is_waiting=True)
    for order in waiting_orders:
        order.is_waiting = False
        customer_email = order.customer.email
        order.save()
        model = instance.model
        version = instance.version
        send_notification(customer_email, model, version)
