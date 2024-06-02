from machine import Pin, ADC, UART
from time import sleep
import network
import espnow

uart = UART(1, baudrate=9600, tx=16, rx=17)

ldr = ADC(Pin(26))
ldr.atten(ADC.ATTN_11DB)

station = network.WLAN(network.STA_IF) 
station.active(True)

esp_now = espnow.ESPNow()
esp_now.active(True)

count = 0

while True:
    try:
        ldr_value = ldr.read()
        if ldr_value > 1000:
            print(ldr_value)
            count += 1  
            print(count)
            sleep(5)
        host, msg = esp_now.recv()
        if msg is not None and b"7c" in msg: 
            print("ESP-NOW Received:", msg)
            uart_message = f"tilfredshed: {msg.decode()} count: {count}"
            uart.write(uart_message.encode())
    
    except Exception as e:
        print("Error:", e)
    
    sleep(1)

