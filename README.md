# MQTT Related Scripts

## RUT240 to ThingsBoard Bridge

The router __RUT240__ is an LTE router so that means that is always will be behind the NAT. Remote access of the router will not be possible but it would be very handy to see the router attributes remotely.

You can easily get the RUT240 atttributes by using their embedded MQTT broker, see the details [here](https://wiki.teltonika-networks.com/view/RUT240_MQTT). 

In case if you have a ThingsBoard setup (or maybe other MQTT dashboard) you can easily publish the obtained attributes with the script [RUT240_ThingsBoard_Bridge.py](https://github.com/aattila/mqtt/blob/master/RUT240_ThingsBoard_Bridge.py). This script is not using any loops it was designed to run regurarly with cron jobs from a device (RaspberryPi) inside in the router's network.
