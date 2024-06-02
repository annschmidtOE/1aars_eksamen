import serial
from time import sleep
import paho.mqtt.publish as publish

data = serial.Serial('/dev/ttyS0', 9600, timeout=2)  

try:
    while True:
        modtaget = data.read()
        if modtaget:
            decoded_modtaget = modtaget.decode('utf-8')
            print(decoded_modtaget)
            payload = decoded_modtaget
            publish.single('7csensor', str(payload), hostname='74.235.100.12') 
        sleep(1)
except KeyboardInterrupt:
    print("Program terminated by user") 
finally:
    data.close()
    print("Serial port closed") 
