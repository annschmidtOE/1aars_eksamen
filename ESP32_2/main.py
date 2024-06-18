from time import sleep
from machine import Pin, ADC, UART
import network
import espnow

uart = UART(1, baudrate=9600, tx=16, rx=17)

led1 = Pin(14, Pin.OUT)

station = network.WLAN(network.STA_IF)
station.active(True)

esp_now = espnow.ESPNow()
esp_now.active(True)

count = 0

ldr = ADC(Pin(35))
ldr.atten(ADC.ATTN_11DB)  

while True:
    try:
        ldr_value = ldr.read()
        print(ldr_value)
        if ldr_value > 1000:
            count += 1
            print(count)
            host, msg = esp_now.recv()
            if msg is not None and "7c" in msg:
                print("ESP-NOW Received:", msg)
                uart.write(bytes(f"{msg} {count}".encode()))
            if count > 10:
                led1.on()
            sleep(5)
    except Exception as e:
        print("Error:", e)
    sleep(1)
