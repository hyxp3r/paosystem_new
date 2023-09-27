import pandas as pd
from django.http import HttpResponse
import base64
from openpyxl.utils import get_column_letter



class XLSX_IO:

    def __init__(self, data) -> None:

        self.data = data
        self.response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.response['Content-Disposition'] = f"attachment; filename=report.xlsx"

    def makeIO(self):
            

        writer = pd.ExcelWriter(self.response, engine='openpyxl')

        self.data.to_excel(writer, index=False, sheet_name='Sheet1')

    
        worksheet = writer.sheets['Sheet1']

        for idx, col in enumerate(self.data):
            series = self.data[col]
            max_len = max((series.astype(str).map(len).max(), len(str(series.name)))) + 5
            if max_len > 50:
                max_len = 50
            col_letter = get_column_letter(idx + 1)
            worksheet.column_dimensions[col_letter].width = max_len
        
        writer.save()
        
        return base64.b64encode(self.response.getvalue()).decode('utf-8')
    
class CSV_IO:

    def __init__(self, data) -> None:

        self.data = data
        self.response = HttpResponse(content_type="application/CSV")
        self.response['Content-Disposition'] = f"attachment; filename=reg.csv"

    def makeIO(self):

        self.data.to_csv(self.response, index=False)

        return base64.b64encode(self.response.getvalue()).decode('utf-8')
        

    
