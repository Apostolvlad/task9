# установка
# 1) pip3 install --upgrade google-api-python-client
# 2) pip3 install oauth2client

# адрес сервисного аккаунта ts-234@task-8-308209.iam.gserviceaccount.com
# гайд https://habr.com/ru/post/483302/


import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

class Table:
    def __init__(self, spreadsheetId = None, table_title = 'Первая таблица', list_title = 'Лист номер один', sheetId = None):
        self.service = self.get_service()
        if spreadsheetId is None:
            spreadsheetId = self.create_table(table_title = table_title, list_title = list_title)
            sheetId = 0
        self.spreadsheetId = spreadsheetId
        if sheetId is None:
            sheetId = self.create_list(list_title)
        self.sheetId = sheetId

    def get_service(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return build('sheets', 'v4', credentials=creds)
    
    def create_table(self, table_title, list_title):
        spreadsheet = self.service.spreadsheets().create(body = {
            'properties': {'title': table_title, 'locale': 'ru_RU'},
            'sheets': [{'properties': {'sheetType': 'GRID',
                                    'sheetId': 0,
                                    'title': list_title,
                                    'gridProperties': {'rowCount': 1, 'columnCount': 1}}}]
        }).execute()
        spreadsheetId = spreadsheet['spreadsheetId']
        print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)
        return spreadsheetId# сохраняем идентификатор файла
    
    def create_list(self, title_list):
        results = self.service.spreadsheets().batchUpdate(
        spreadsheetId = self.spreadsheetId,
        body = {
            "requests": [
                {
                "addSheet": {
                    "properties": {
                    "title": title_list,
                    "gridProperties": {
                        "rowCount": 100,
                        "columnCount": 30
                    }
                    }
                }
                }
            ]
            }).execute() #'replies': [{'addSheet': {'properties': {'sheetId
        return results['replies'][0]['addSheet']['properties']['sheetId']

    def list_table(self):
       # Fetch the document to determine the current indexes of the named ranges.
        document = self.service.spreadsheets().sheets()#.get(spreadsheetId  = self.spreadsheetId)
        print(dir(document))


    def update_values(self, data, list_range = "Лист номер один!B2:D5"):
        results = self.service.spreadsheets().values().batchUpdate(spreadsheetId = self.spreadsheetId, body = {
            "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": [
                {
                    "range": list_range, 
                "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
                "values": data
                }
            ]
        }).execute()
        print(results)
    
    def set_size_colomn(self):
        self.service.spreadsheets().batchUpdate(spreadsheetId = self.spreadsheetId, body = {
            "requests": [
                {
                    "updateDimensionProperties": {
                        "range": {
                        "sheetId": self.sheetId,
                        "dimension": "COLUMNS",  # Задаем ширину колонки
                        "startIndex": 0, # Нумерация начинается с нуля
                        "endIndex": 2 # Со столбца номер startIndex по endIndex - 1 (endIndex не входит!)
                        },
                        "properties": {
                        "pixelSize": 250 # Ширина в пикселях
                        },
                        "fields": "pixelSize" # Указываем, что нужно использовать параметр pixelSize  
                    }
                },
            ]}
        ).execute()
    
    def set_format_Cell(self, cells):
        requests = list()
        for cell in cells:
            setting_cell = {
                "repeatCell": 
                {
                    "cell": 
                    {
                    "userEnteredFormat": 
                    {
                        "backgroundColor": {
                            "red": 0.2,
                            "green": 0.7,
                            "blue": 0.2,
                            "alpha": 1
                        },
                    }
                    },
                    "range":{
                        "sheetId": self.sheetId,
                        "startRowIndex": cell[0],
                        "endRowIndex": cell[0] + 1,
                        "startColumnIndex": cell[1],
                        "endColumnIndex": cell[1] + 2
                    },
                    "fields": "userEnteredFormat"
                }
            }
            requests.append(setting_cell)
        results = self.service.spreadsheets().batchUpdate(spreadsheetId = self.spreadsheetId, body = {"requests": requests}).execute()


if __name__ == '__main__':
    table = Table('1utinFVgu39rsTpZRKim5lsqtquFRdsFG2EXYQFyC5hg') #main()
    table.list_table()

