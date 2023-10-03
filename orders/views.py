import json
from http import HTTPStatus

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .forms import OrderForm
from .models import Order
from robots.models import Robot


class CreateOrderView(View):
    """Вьюкласс создания заказа."""

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CreateOrderView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            form = OrderForm(data)

            if form.is_valid():
                robot_serial = data.get('robot_serial')
                if Robot.objects.filter(serial=robot_serial).exists():
                    form.save()
                    response_data = {'success': 'Order saved successfully'}
                else:
                    order = form.save(commit=False)
                    order.is_waiting = True
                    order.save()
                    response_data = {'message': 'Robot is out of stock'}
                return JsonResponse(response_data, status=HTTPStatus.CREATED)
            else:
                return JsonResponse({'error': form.errors}, status=HTTPStatus.BAD_REQUEST)
        except AttributeError as e:
            return JsonResponse({'error': str(e)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

