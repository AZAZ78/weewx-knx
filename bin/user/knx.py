# Copyright 2017-2020 Alexander Zeh
# weewx module that writes weather information to knx bus
# Its necessary to install pknx to use this service

import syslog
from distutils.version import StrictVersion

import weewx.engine
import weewx.units
import weeutil.config

from knxip.ip import KNXIPTunnel
from knxip.conversion import float_to_knx2, knx2_to_float, \
    knx_to_time, time_to_knx, knx_to_date, date_to_knx, datetime_to_knx,\
    knx_to_datetime
from knxip.core import KNXException, parse_group_address

VERSION = "0.1"
REQUIRED_WEEWX = "3.6.1"
REQUIRED_KNXIP = "0.3.2"

if StrictVersion(weewx.__version__) < StrictVersion(REQUIRED_WEEWX):
    raise weewx.UnsupportedFeature("weewx %s or greater is required, found %s"
                                   % (REQUIRED_WEEWX, weewx.__version__))

#if StrictVersion(knxip.__version__) < StrictVersion(REQUIRED_KNXIP):
#    raise weewx.UnsupportedFeature("knxip %s or greater is required, found %s"
#                                   % (REQUIRED_KNXIP, knxip.__version__))
                                   
try:
    # Test for new-style weewx logging by trying to import weeutil.logger
    import weeutil.logger
    import logging
    log = logging.getLogger(__name__)

    def logdbg(msg):
        log.debug(msg)

    def loginf(msg):
        log.info(msg)

    def logerr(msg):
        log.error(msg)

except ImportError:
    # Old-style weewx logging
    import syslog

    def logmsg(level, msg):
        syslog.syslog(level, 'weewx-knx: %s:' % msg)

    def logdbg(msg):
        logmsg(syslog.LOG_DEBUG, msg)

    def loginf(msg):
        logmsg(syslog.LOG_INFO, msg)

    def logerr(msg):
        logmsg(syslog.LOG_ERR, msg)                                   

class KNX(weewx.engine.StdService):
    def __init__(self, engine, config_dict):
        super(KNX, self).__init__(engine, config_dict)
        conf = config_dict['KNX']
        
        # Read default information for gateway
        self._gateway_ip = conf['gateway_ip']
        self._gateway_port = int(conf.get('gateway_port', 3671))
        
        
        # Read the mapping information for KNX and store them locally
        self._knx_map = weeutil.config.deep_copy(conf);
        del self._knx_map['gateway_ip']
        del self._knx_map['gateway_port']
        
        self._knx_tunnel = KNXIPTunnel(self._gateway_ip, self._gateway_port)
        
        self.bind(weewx.NEW_ARCHIVE_RECORD, self._handle_new_archive_record)
        
        loginf('Started knx extension for weewx with gateway {0}'.format(self._gateway_ip))
        if self._gateway_ip == '0.0.0.0':
            loginf('Will try to auto-detect KNX/IP gateway')

    def _handle_new_archive_record(self, event):
        record = event.record
        tunnel = self._knx_tunnel

        try:
            res = tunnel.connect()
            if not res:
                logerr('Could not connect to KNX/IP interface {0}, retry later'.format(self._gateway_ip))
                return
        except KNXException as ex:
            logerr('Exception during connect to KNX/IP interface {0}: {1}, retry later'.format(self._gateway_ip, ex))
            return

        try:
            for key, value in self._knx_map.items():
                data = record.get(key)
                if data is not None:
                    logdbg('Send {0} with data {1} to address {2}'.format(key, data, value))
                    encoded_data = float_to_knx2(float(data))
                    tunnel.group_write(parse_group_address(value), encoded_data)
                else:
                    logerr('No value available for {0} and address {1}, nothing send'.format(key, value))

        except KNXException as ex:
            logerr('KNXException raised : {0}'.format(ex))

        try:
            tunnel.disconnect() 
        except KNXException as ex:
            logerr('KNXException raised : {0}'.format(ex))

