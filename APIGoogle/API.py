from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import date

def GetSheet():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'keys.json'
    
    #creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    
    spreadsheetId = '12Z6D5AXPM0cPJo9TBYFp5aaNkr90xPmdJUYzel46cLA'
    
    service = build('sheets', 'v4', credentials=creds)
    
    # Call the Sheets API
    sheet = service.spreadsheets()
    
    return sheet, spreadsheetId


def GetActives():
    sheet, spreadsheetId = GetSheet()
    result = sheet.values().get(spreadsheetId=spreadsheetId,
                                range="ativos!1:1000",
                                majorDimension="ROWS").execute()
    
    values = result.get('values', [])
    
    actives = []
    for i in values:
        if i[0] == "FALSE":
            actives.append(i)
    
    return actives


def SetNew(tipo, sequencia, frase1, frase2,frase3):
    sheet, spreadsheetId = GetSheet()
    result = sheet.values().get(spreadsheetId=spreadsheetId,
                                range="ativos!1:1000",
                                majorDimension="ROWS").execute()
    
    values = result.get('values', [])
    
    lr = len(values)+1
    Range = "ativos!A" + str(lr)
    
    values.reverse()    
    for row in values:
        ID = row[1]
        
        if ID[0] == tipo:    
            ID = int(ID[1:])+1
            ID = f"{tipo}{ID}"
            values.reverse()
            break
        
    today = date.today().strftime("%d/%m/%Y")
    newRow = [[False, ID, tipo, sequencia, frase1, frase2, frase3, today]]
    
    sheet.values().update(spreadsheetId=spreadsheetId,
                                    range=Range,
                                    valueInputOption="USER_ENTERED",
                                    body={"values": newRow}).execute()



#print(GetActives())
#SetNew("c","A","oi","mundo","!!!")