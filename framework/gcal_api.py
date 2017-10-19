from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import os
import httplib2

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class GCalAPI:
    def __init__(self, client_secret_file):
        """
        Define General parameters
        """
        # Which scope from Google to use (https://developers.google.com/gmail/api/auth/scopes)
        self.SCOPES = 'https://www.googleapis.com/auth/calendar'
        # The API Secret File
        self.CLIENT_SECRET_FILE = client_secret_file
        self.APPLICATION_NAME = 'Clearslide GCal API'

    def _get_credentials(self):
        """
        Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        :return: credentials
        """

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'python-gcal.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE,
                                                  self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + credential_path)
        return credentials

    def _build_service(self):
        """
        Build a GMail service

        :return: service
        """
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        return service

    def list_calendars(self):
        service = self._build_service()

        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print(calendar_list_entry['summary'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    def get_events_list(self, calid, tmin):
        service = self._build_service()

        events_results = service.events().list(
            calendarId=calid, timeMin=tmin, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()

        events = events_results.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    def create_event(self, calid, summary, description, start,
                     end, notifications=False):
        evnt = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start
            },
            'end': {
                'dateTime': end
            }
        }

        service = self._build_service()

        event = service.events().insert(calendarId=calid, body=evnt,
                                        sendNotifications=notifications).execute()

        print('Event created: {}'.format(event.get('htmlLink')))


