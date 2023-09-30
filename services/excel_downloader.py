from openpyxl import Workbook


class RobotExcelDownloader:
    """Класс для создания excel-файла по суммарным показателям производства роботов."""

    def __init__(self, queryset):
        self.queryset = queryset

    def generate_excel(self):
        model_data = {}
        for entry in self.queryset:
            model = entry['model']
            if model not in model_data:
                model_data[model] = []
            model_data[model].append(
                {
                    'model': entry['model'],
                    'version': entry['version'],
                    'count': entry['count']
                }
            )

        wb = Workbook()
        wb.remove(wb.active)

        for model, data in model_data.items():
            self.add_data_to_sheet(wb, model, data)
        return wb

    def add_data_to_sheet(self, workbook, sheet_name, data):
        sheet = workbook.create_sheet(sheet_name)
        header_row = ['Модель', 'Версия', 'Количество за неделю']
        sheet.append(header_row)

        for entry in data:
            row = [entry['model'], entry['version'], entry['count']]
            sheet.append(row)
