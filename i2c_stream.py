import data_collector
import serial
import serial.tools.list_ports
import threading
import json
from time import sleep
from smbus import SMBus
import struct
import board
from adafruit_seesaw import seesaw, rotaryio, digitalio
#import adafruit_am2320
import time
import adafruit_sht31d
#import busio

bus = SMBus(1)
i2c = board.I2C()
#seesaw = seesaw.Seesaw(i2c, addr=0x36)
#am = adafruit_am2320.AM2320(i2c)
#sensor = adafruit_sht31d.SHT31D(i2c)

#seesaw.pin_mode(24, seesaw.INPUT_PULLUP)

#encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = 0
class feedRate():
    def __init__(self, _sensorName, lastPos):
        self.sensorName = _sensorName
        self.lastPos = lastPos
    def __str__(self):
        return f'{self.sensorName}'
    def feedRead(self):
        position = -encoder.position
        if position != self.lastPos:
            self.lastPos = position
        return position
     
class DHTsensorTemp():
    def __init__(self, _sensorName):
        self.sensorName = _sensorName
    def __str__(self):
        return f'{self.sensorName}'
    def DHTRead(self):
        return sensor.temperature
        #('Temperature: {0}C'.format(sensor.temperature));
class DHTsensorHumidity():
    def __init__(self, _sensorName):
        self.sensorName = _sensorName
    def __str__(self):
        return f'{self.sensorName}'
    def DHTRead(self):
        return sensor.relative_humidity
    #('Temperature: {0}C'.format(sensor.temperature));
         
class I2CFloatPublisher():
    def __init__(self, _sensorName, _address):
        self.sensorName = _sensorName
        self.address = _address
    def __str__(self):
        #return object name
        return f'{self.sensorName}'	
    def i2cRead(self):
    #with SMBus(1) as bus:
     # Read a block of 16 bytes from address 80, offset 0
        #value = my_bus.read_byte(self.address) ### This works.
        while True:
            try:
                value = bytes(bus.read_i2c_block_data(self.address, 99, 4))
                return struct.unpack('f', value)[0]
            except:
                pass
        
        #time.sleep(0.005)
            # Returned value is a list of 4 bytes

#feedRateSensor = feedRate("Feed Rate", 0)
#sensor1 = I2CFloatPublisher("Current1", 0x15, 99)
#temp = DHTsensorTemp("Temp: ")
#humidity = DHTsensorHumidity("Humidity: ")
sensor2 = I2CFloatPublisher("Current2", 0x15)



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
        #print(f'{temp}{temp.DHTRead()} ; {humidity}{humidity.DHTRead()} ; {feedRateSensor}:{feedRateSensor.feedRead()} ; {sensor1}:{sensor1.i2cRead()} ; {sensor2}:{sensor2.i2cRead()} ; {sensor3}:{sensor3.i2cRead()} ; {sensor4}:{sensor4.i2cRead()} ; {sensor5}:{sensor5.i2cRead()} ; {sensor6}:{sensor6.i2cRead()} ; {sensor7}:{sensor7.i2cRead()}')
        print(f'{sensor2}:{sensor2.i2cRead()}')
        #data_collector.record_metric(feedRateSensor.sensorName, feedRateSensor.feedRead())
        #data_collector.record_metric(sensor1.sensorName, sensor1.i2cRead())
        data_collector.record_metric(sensor2.sensorName, sensor2.i2cRead())
       #data_collector.record_metric(temp.sensorName, temp.DHTRead())
        #data_collector.record_metric(humidity.sensorName, humidity.DHTRead())
        #data_collector.record_metric(sensor3.sensorName, sensor3.i2cRead())
        #data_collector.record_metric(sensor4.sensorName, sensor4.i2cRead())
        #data_collector.record_metric(sensor5.sensorName, sensor5.i2cRead())
        #data_collector.record_metric(sensor6.sensorName, sensor6.i2cRead())
        #data_collector.record_metric(sensor7.sensorName, sensor7.i2cRead())
                #START HERE
                
        
    #_dat.conn.close()
    #_dat.conn = None
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

    _dat.thread = threading.Thread(target=stream_loop)
    _dat.thread.name = 'i2c_stream'
    _dat.thread.start()

def stop_streaming():
    with _dat.terminate_lock:
        if not _dat.terminate:
            _dat.terminate = True
