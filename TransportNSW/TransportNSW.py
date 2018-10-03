"""A module to query Transport NSW (Australia) departure times."""
from datetime import timedelta, datetime
from requests.exceptions import ConnectionError
import requests
import logging

ATTR_STOP_ID = 'stopid'
ATTR_ROUTE = 'route'
ATTR_DUE_IN = 'due'
ATTR_DELAY = 'delay'
ATTR_REALTIME = 'realtime'


class TransportNSW(object):
    """The Class for handling the data retrieval."""

    def __init__(self):
        """Initialize the data object."""
        self.stopid = None
        self.route = None
        self.apikey = None
        self.info = [{
            ATTR_STOP_ID: None,
            ATTR_ROUTE: None,
            ATTR_DUE_IN: 'n/a',
            ATTR_DELAY: 'n/a',
            ATTR_REALTIME: 'n/a',
            }]

    def get_departures(self, stopid, route, apikey):
        """Get the latest data from Transport NSW."""
        self.stopid = stopid
        self.route = route
        self.apikey = apikey

        # Build the URL including the STOPID and the API key
        url = \
            'https://api.transport.nsw.gov.au/v1/tp/departure_mon?' \
            'outputFormat=rapidJSON&coordOutputFormat=EPSG%3A4326&' \
            'mode=direct&type_dm=stop&name_dm=' \
            + self.stopid \
            + '&departureMonitorMacro=true&TfNSWDM=true&version=10.2.1.42'
        auth = 'apikey ' + self.apikey
        header = {'Accept': 'application/json', 'Authorization': auth}

        try:
            response = requests.get(url, headers=header, timeout=10)
        except ConnectionError as e:
            logging.warning("Network error")
            self.info = [{
                ATTR_STOP_ID: 'n/a',
                ATTR_ROUTE: 'n/a',
                ATTR_DUE_IN: 'n/a',
                ATTR_DELAY: 'n/a',
                ATTR_REALTIME: 'n/a',
                }]
            return self.info

        # If there is no valid request, set to default response
        if response.status_code != 200:
            logging.warning("Error with the request sent; check api key")
            self.info = [{
                ATTR_STOP_ID: 'n/a',
                ATTR_ROUTE: 'n/a',
                ATTR_DUE_IN: 'n/a',
                ATTR_DELAY: 'n/a',
                ATTR_REALTIME: 'n/a',
                }]
            return self.info

        # Parse the result as a JSON object
        result = response.json()

        # If there is no stop events for the query, set to default response
        try:
            result['stopEvents']
        except KeyError:
            # logging.warning("No stop events for this query")
            self.info = [{
                ATTR_STOP_ID: 'n/a',
                ATTR_ROUTE: 'n/a',
                ATTR_DUE_IN: 'n/a',
                ATTR_DELAY: 'n/a',
                ATTR_REALTIME: 'n/a',
                }]
            return self.info

        # Set variables
        maxresults = 3
        monitor = []
        if self.route != '':
            # Find the next stop events for a specific route
            for i in range(len(result['stopEvents'])):
                number = result['stopEvents'][i]['transportation']['number']
                if number == self.route:
                    event = self.parseEvent(result, i)
                    if event != None:
                        monitor.append(event)
                    if len(monitor) >= maxresults:
                        # We found enough results, lets stop
                        break
        else:
            # No route defined, find any route leaving next
            for i in range(0, maxresults):
                event = self.parseEvent(result, i)
                if event != None:
                    monitor.append(event)
        if monitor:
            self.info = [{
                ATTR_STOP_ID: self.stopid,
                ATTR_ROUTE: monitor[0][0],
                ATTR_DUE_IN: monitor[0][1],
                ATTR_DELAY: monitor[0][2],
                ATTR_REALTIME: monitor[0][5],
                }]
        else:
            # No stop events for this route
            self.info = [{
                ATTR_STOP_ID: 'n/a',
                ATTR_ROUTE: 'n/a',
                ATTR_DUE_IN: 'n/a',
                ATTR_DELAY: 'n/a',
                ATTR_REALTIME: 'n/a',
                }]
        return self.info

    def parseEvent(self, result, i):
        """Parse the current event and extract data"""
        fmt = '%Y-%m-%dT%H:%M:%SZ'
        due = 0
        delay = 0
        realtime = 'n'
        number = result['stopEvents'][i]['transportation']['number']
        planned = datetime.strptime(result['stopEvents'][i]
            ['departureTimePlanned'], fmt)
        estimated = planned
        if 'isRealtimeControlled' in result['stopEvents'][i]:
            realtime = 'y'
            estimated = datetime.strptime(result['stopEvents'][i]
                ['departureTimeEstimated'], fmt)
        # Only deal with future leave times
        if estimated > datetime.utcnow():
            due = self.get_due(estimated)
            delay = self.get_delay(planned, estimated)
            return[
                number,
                due,
                delay,
                planned,
                estimated,
                realtime,
                ]
        else:
            return None

    def get_due(self, estimated):
        """Min till next leave event"""
        due = 0
        due = round((estimated - datetime.utcnow()).seconds / 60)
        return due

    def get_delay(self, planned, estimated):
        """Min of delay on planned departure"""
        delay = 0
        if estimated >= planned:
            delay = round((estimated - planned).seconds / 60)
        else:
            delay = round((planned - estimated).seconds / 60) * -1
        return delay
