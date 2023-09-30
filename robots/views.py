import json
from datetime import timedelta
from http import HTTPStatus

from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from services.excel_downloader import RobotExcelDownloader

from .forms import RobotForm
from .models import Robot


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


class RobotExcelView(View):
    """Вьюкласс формирования excel-файла с отчетом по производству роботов
       за последнюю прошедшую неделю."""
    def get(self, request, *args, **kwargs):
        current_datetime = timezone.now()
        start_of_week = current_datetime - timedelta(days=current_datetime.weekday()+7)
        end_of_week = start_of_week + timedelta(days=7)

        queryset = Robot.objects.filter(
            created__gte=start_of_week,
            created__lte=end_of_week
        ).values('model', 'version').annotate(count=Count('id'))

        excel_downloader = RobotExcelDownloader(queryset)
        wb = excel_downloader.generate_excel()
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=robots_counts.xlsx'
        wb.save(response)

        return response
