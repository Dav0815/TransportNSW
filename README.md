# TransportNSW
Python lib to access Transport NSW information.

## How to Use

### Get your API Key
An OpenData account and API key is required to request the data. More information on how to create the free account can be found here.
https://opendata.transport.nsw.gov.au/user-guide

### Get your stop and line
The libary will expect at least stop id to request the next leave events. The easieste way to get the ID is using Google Maps and clicking on one of the bus, train or ferry stops. The information pane one the left will show the relevant stop ID.

Another source for the stop ID and line is  https://transportnsw.info/stops#/. It provides the option to search for a stop and the corresponding lines leaving from there. 

### Sample Code
The following example will request the next leave event for the bus line *199* from stop ID *209516*.

**Code:**
```python
from TransportNSW import TransportNSW
ptnsw1 = TransportNSW.TransportNSW()
journey = tnsw.get_departures('209516','199','YOUR_API_KEY')
print(journey)
```
**Result:**
```
{'stopid': '209516', 'route': '199', 'due': 16, 'delay': 6, 'realtime': 'y'}
```
* route: bus, train, ferry number
* due: minutes till next leave
* realtime: flag if the leave event has realtime information
* delay: delay in minutes from the scheduled leave time

Leaving the line field empty will return any bus/train/ferry leaving next from a given stop.
**Code:**

```python
journey = tnsw.get_departures('209516','','YOUR_API_KEY')
```

### Errors

No leave event with wrong stop ID or not matching route.
```
{'stopid': 'n/a', 'route': 'n/a', 'due': 'n/a', 'delay': 'n/a', 'realtime': 'n/a'}
```
