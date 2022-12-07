from json.decoder import JSONDecodeError
import data_collector
import serial
import serial.tools.list_ports
import threading
import json
import time
from smbus import SMBus
import struct

bus = SMBus(1)

class I2CFloatPublisher():
    def __init__(self, _sensorName, _address, _ret):
        self.sensorName = _sensorName
        self.address = _address
        self.ret = _ret
    def __str__(self):
        #return object name
        return f'{self.sensorName}'
    def i2cRead(self):
    #with SMBus(1) as bus:
        # Read a block of 16 bytes from address 80, offset 0
        value = bus.read_i2c_block_data(self.address, self.ret, 4)
        return struct.unpack('f', bytes(value))[0]
            # Returned value is a list of 4 bytes

sensor1 = I2CFloatPublisher("Current1", 0x08, 99)
sensor2 = I2CFloatPublisher("Current2", 0x09, 99)
# sensor3 = I2CFloatPublisher("Current3", 0x11)
# sensor4 = I2CFloatPublisher("Current4", 0x12)
# sensor5 = I2CFloatPublisher("Current5", 0x13)


class Data():
    def __init__(self) -> None:
        self.thread = None
        self.terminate_lock = threading.Lock()
        self.terminate = False
        self.logger = None

_dat = Data()

def stream_loop():
    _dat.logger.info('[i2c] Started Streaming')
    #count iterations of stream_loop
    #get start time
    #track elapsed time
    # print iterations and elapsed time
    while True:
        with _dat.terminate_lock:
            if _dat.terminate:
                break
        print(f'{sensor1}:{sensor1.i2cRead()} ; {sensor2}:{sensor2.i2cRead()} ; {sensor3}:{sensor3.i2cRead()}')
        #{sensor2}: {sensor2.i2cRead()}, {sensor3}: {sensor3.i2cRead()}')
        data_collector.record_metric(sensor1.sensorName, sensor1.i2cRead())
        data_collector.record_metric(sensor2.sensorName, sensor2.i2cRead())
        #data_collector.record_metric(sensor3.sensorName, sensor3.i2cRead())
        #data_collector.record_metric(sensor4.sensorName, sensor4.i2cRead())
                #START HERE
               
    _dat.logger.info(f'[i2c] Stopped streaming..')

def get_ports():
    ports = serial.tools.list_ports.comports()
    devices = map(lambda p : p.device, ports)
    return list(devices)

def start_streaming(logger): #delete sensors
    #get current time
    _dat.logger = logger
    with _dat.terminate_lock:
        _dat.terminate = False

    _dat.thread = threading.Thread(target=stream_loop, args=[])
    _dat.thread.name = 'i2c_stream'
    _dat.thread.start()

def stop_streaming():
    with _dat.terminate_lock:
        if not _dat.terminate:
            _dat.terminate = True
