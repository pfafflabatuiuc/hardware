import logging
import qcodes
from qcodes import (Instrument, validators as vals)
from py_thorlabs_tsp import ThorlabsTsp01B as _TSP

logger = logging.getLogger(__name__)

class ThorLabs_TSP01B(Instrument):

    def __init__(self, name, serial=None, **kwargs):

        # if serial is None:
        #     raise Exception('TSP01 serial number needed!')

        logger.info(__name__ + f' : Initializing instrument TSP01 {serial}')
        super().__init__(name, **kwargs)

        # serial number on sensor
        self.sensor = _TSP(serial)

        # first temperature measure (sensor inside USB device)
        self.add_parameter('temperature_1',
                           get_cmd=self.measure_temp1,
                           set_cmd=False,
                           vals=vals.Numbers(),
                           get_parser=float,
                           unit='C')

        # second temperature measure (first external sensor)
        self.add_parameter('temperature_2',
                           get_cmd=self.measure_temp2,
                           set_cmd=False,
                           vals=vals.Numbers(),
                           get_parser=float,
                           unit='C')

        # # third temperature measure (second external sensor) - NOT USED CURRENTLY
        # self.add_parameter('temp3',
        #                    get_cmd=self.measure_temp3,
        #                    set_cmd=False,
        #                    vals=vals.Numbers(),
        #                    get_parser=float,
        #                    unit='C')

        # humidity measure (sensor inside USB device)
        # units of relative humidity (percentage value)
        self.add_parameter('humidity',
                           get_cmd=self.measure_humid,
                           set_cmd=False,
                           vals=vals.Numbers(),
                           get_parser=float,
                           unit='RH')

        self.connect_message()

    def get_idn(self):
        return {
            "vendor": "ThorLabs",
            "model:": "TSP-01B",
            "serial": "M00885311",
            "firmware": None
        }

    def measure_temp1(self):
        return self.sensor.measure_temperature('th0')

    def measure_temp2(self):
        return self.sensor.measure_temperature('th1')

    def measure_temp3(self):
        return self.sensor.measure_temperature('th2')

    def measure_humid(self):
        return self.sensor.measure_humidity()
