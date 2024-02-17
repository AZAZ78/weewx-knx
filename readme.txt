knx - weewx extension for generating EIBnet/IP packets
Copyright 2024 Alexander Zeh
Distributed under terms of the GPLv3

This weewx[1] extension allows the generation of EIBnet/IP packets
containing weather information collected by weewx.
This extension was written for the purpose of easy integration with EIB home automation.
When this extension is enabled, weewx will generate a new EIBnet/IP packet every
StdArchive.archive_interval seconds.

A knxd[3] can be used as EIBnet/IP bridge for usb and serial interfaces.

Prerequisits:
    knx library for python: pip3 install knx

Installation:
    weectl extension install weewx-knx.tar.gz    

Configuration:
    [KNX]
		# EIBnet/IP gateway configuration
		gateway_ip = 192.168.2.70
		gateway_port = 6720

		# node configuration
		outTemp = 5.5.150
		wind = 5.5.151
		windGust = 5.5.152
		rainRate = 5.5.153
		outHumidity = 5.5.154

[1] http://www.weewx.com/
[3] https://github.com/knxd/knxd
