# MQTT Related Scripts

## RUT240 to ThingsBoard Bridge

The router __RUT240__ is an LTE router so that means that is always will be behind the NAT. Directly acessing will not be possible but it is very handy to see the router attributes remotelly.
You can easily get the RUT240 atttributes by using their embedded MQTT broker, see the details [here](https://wiki.teltonika-networks.com/view/RUT240_MQTT). 
In case if you have a ThingsBoard setup (or maybe other MQTT dashboard) you can easily publish the obtained attributes with the script [RUT24_ThingsBoard_Bridge.py](https://github.com/aattila/mqtt/blob/master/RUT24_ThingsBoard_Bridge.py).

