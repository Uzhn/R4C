import json
from http import HTTPStatus
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Robot
from .forms import RobotForm


class RobotAPIView(View):
    """Вьюкласс робота."""
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(RobotAPIView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            form = RobotForm(data)

            if form.is_valid():
                form.save()
                response_data = {'success': 'Robot data saved successfully'}
                return JsonResponse(response_data, status=HTTPStatus.CREATED)
            else:
                return JsonResponse({'error': form.errors}, status=HTTPStatus.BAD_REQUEST)
        except AttributeError as e:
            return JsonResponse({'error': str(e)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
