# BSD 3-Clause License
# Copyright (c) 2019, Hugonun(https://github.com/hugonun)
# All rights reserved.

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class gsheet(object):
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('sheets', 'v4', credentials=self.creds)

    def add(self,sheetid,sheetrange,ivalue):
        # Call the Sheets API
        sheet = self.service.spreadsheets()
        values = []
        values.append(ivalue)
        body = {
            'values': values
        }
        result = sheet.values().append(
            spreadsheetId=sheetid, range=sheetrange,
            valueInputOption='RAW', body=body).execute()
        
    def last(self,sheetid):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=sheetid, range="A1:D1000").execute()
        print(result)
        source = list(result.values())[2]
        lastRow = source[len(source)-1]
        print(lastRow)
        return lastRow 
    
    def find(self,sheetid,uid):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=sheetid, range="A1:D1000").execute()
        print(result)
        source = list(result.values())[2]
        foundRow = [0,0,0,0]
        for i in range(0,len(source)):
            j = source[i]
            if j[1] == uid:
                foundRow = j
                break
            i = i + 1
        if foundRow == [0,0,0,0]:
            return "nope"
        while len(foundRow) < 4:
            foundRow.append("N/A")
        return foundRow
    
    def row(self,sheetid,row):
        sheet = self.service.spreadsheets()
        parseableRow = "A"+row+":D"+row
        result = sheet.values().get(
            spreadsheetId=sheetid, range=parseableRow).execute()
        print(result)
        if len(list(result.values())) < 3:
            return "nope"
        source = list(result.values())[2]
        print(source)
        onlySource = source[0]
        while len(onlySource) < 4:
            onlySource.append("N/A")
        return onlySource