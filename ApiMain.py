from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools



def get_google_sheet(spreadsheet_id, range_name):
    """ Retrieve sheet data using OAuth credentials and Google Python API. """
    scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    # Setup the Sheets API
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name)
    response = gsheet.execute()
    return response

def append_value(spreadsheet_id, range_name, values):

    scopes = 'https://www.googleapis.com/auth/spreadsheets'

    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_name, body=values, valueInputOption='USER_ENTERED', insertDataOption='OVERWRITE')
    response = request.execute()


#SPREADSHEET_ID = '1AtwgdRFTtqv-Y1kq3eUPFivaFd8nudzyO0XGKrvo4j0'
#RANGE_NAME = 'assitence1'

#append_value(SPREADSHEET_ID, RANGE_NAME, resource)
#gsheet = get_google_sheet(SPREADSHEET_ID, RANGE_NAME)

