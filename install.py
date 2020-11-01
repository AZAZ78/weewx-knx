# installer for weewx-knx
# Copyright 2020 Alexander Zeh
# Distributed under the terms of the GNU Public License (GPLv3)

from setup import ExtensionInstaller


def loader():
    return KNXInstaller()


class KNXInstaller(ExtensionInstaller):
    def __init__(self):
        super(KNXInstaller, self).__init__(
            version='0.1',
            name='weewx_knx',
            description='Write weather information to knx bus',
            author='Alexander Zeh',
            author_email='alex.zeh@web.de',
            process_services='user.knx.KNX',
            config={
                'KNX': {
					'gateway_ip': '192.168.2.70',
					'gateway_port': 3671,
					'outTemp': '5.5.150',
					'windSpeed': '5.5.151',
					'windGust': '5.5.152',
					'hourRain': '5.5.153',
					'outHumidity': '5.5.154',
                },
            },
            files=[('bin/user', ['bin/user/knx.py'])]
        )
