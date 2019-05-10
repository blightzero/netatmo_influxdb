# netatmo_influxdb
Simple script that pulls weather data from netatmo nodes via the public web API and pushes it into your local influxdb.

## Getting device ids
Visiting the Netatmo Weather map (https://weathermap.netatmo.com/) one can search for and select local nodes.
On selecting a node an HTTP request can be observed via the developer tools to the API:
https://app.netatmo.net/api/getmeasure
The device id of the selected node will be transmitted.

Alternatively you can search for nodes in your aread via the API with a curl command similar to this:

```
curl -H 'Authorization: Bearer 52d42f05177759882c8b456a|753293ecafa4f4b1a9604611adc998e9' \
'https://app.netatmo.net/api/getpublicmeasures?date_end=last&divider=3&lat_ne=50.93381327191293&lat_sw=50.90688748924506&limit=2&lon_ne=6.943359375&lon_sw=6.932373046875&quality=7&zoom=15'\
|jq '.body[]|._id,.modules'
```
Just change the logditude and latitude values accordingly!

