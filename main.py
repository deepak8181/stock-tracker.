import requests
from requests.models import Response
from time import sleep
from google.oauth2 import service_account
from googleapiclient.discovery import build
import itertools

##### google api   start####
SCOPES = ['https://www.googleapis.com/auth/']

SAMPLE_SPREADSHEET_ID = 'write here your sample spreadsheet id'
SERVICE_ACCOUNT_FILE='keys.json'
creds = None
creds=service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
   
    
service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()
### end####

STOCK_NAME = ["TCS","AMZN","TSLA","TWTR","AMC","AMD","MSFT","FB","NFLX","AAPL","QQQ","SPY","NVDA","GME","NIO"]
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_api_key="write here your stock api key"

stock_params={
        "function":"TIME_SERIES_DAILY",
        "symbol":STOCK_NAME,
        "apikey":stock_api_key,
    }

response=requests.get(STOCK_ENDPOINT, params=stock_params)
da = response.json()["Time Series (Daily)"]
# da = response.json()
# print(da)
lis=[[key for (key, value) in da.items()]]
result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range="Sheet1!B1", valueInputOption="USER_ENTERED", body={"values":lis}).execute()

print(result)
sleep(12)

row_name="Sheet1!A2","Sheet1!A3","Sheet1!A4","Sheet1!A5","Sheet1!A6","Sheet1!A7","Sheet1!A8","Sheet1!A9","Sheet1!A10","Sheet1!A11","Sheet1!A12","Sheet1!A13","Sheet1!A14","Sheet1!A15","Sheet1!A16"

#### we use here double loop###
for (stock, row) in itertools.zip_longest(STOCK_NAME, row_name) :

    stock_params={
        "function":"TIME_SERIES_DAILY",
        "symbol":stock,
        "apikey":stock_api_key,
    }
    response=requests.get(STOCK_ENDPOINT, params=stock_params)
    data= response.json()["Time Series (Daily)"]
    data_list=[value for (key, value) in data.items()]
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    SAMPLE_SPREADSHEET_ID = ''
    SERVICE_ACCOUNT_FILE='keys.json'
    creds = None
    creds=service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    rateprice=[stock]
    gupta=[rateprice]
    
        
    
    for dat in data_list:
        yesterdy_data=dat
        yesterday_closing_prige=yesterdy_data["4. close"]
        rateprice.append(yesterday_closing_prige)
        # TATA=[yesterday_closing_prige]
        


    resul = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                    range=row,valueInputOption="USER_ENTERED", body={"values":gupta}).execute()

    # print(resul)
    # print(gupta)
    sleep(12)
