# TransportNSW
Python lib to access Transport NSW information

# How to Use

## 1 Get your API Key
In order to access the Transport NSW information, you have to register and generate an API key.
[https://opendata.transport.nsw.gov.au/user-guide] (https://opendata.transport.nsw.gov.au/user-guide)

## 2 Get your stop and line
The libary will expect at least stop id to request the next leave events. The easieste way to get the ID is using Google Maps and clicking on one of the bus, train or ferry stops. The information pane one the left will show you the relevant stop ID.

## 3 test.py
With the API you can now setup your first test code. 

The following example will request the next leave event for the bus line *199* from stop ID *209516*.

**Code:**
```python
from TransportNSW import TransportNSW
p1 = TransportNSW.TransportNSW()
journey = p1.get_departures('209516','199','YOUR_API_KEY')
print(journey)
```
**Result:**
```
No language indicated, so no syntax highlighting. 
But let's throw in a <b>tag</b>.
```
You can request any bus/train/ferry leaving from a given stop by leaving the line empty
**Code:**

```python
journey = p1.get_departures('209516','','YOUR_API_KEY')
```
**Result:**
```
No language indicated, so no syntax highlighting. 
But let's throw in a <b>tag</b>.
```
