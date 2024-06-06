from time import sleep
from machine import Pin, ADC, UART

ldr = ADC(Pin(26))
ldr.atten(ADC.ATTN_11DB)

uart = UART(1, baudrate=9600, tx=16, rx=17)
led1 = Pin(14, Pin.OUT)

count = 0

while True:
    try:
        ldr_value = ldr.read()
        print(ldr_value)
        if ldr_value > 1000:
            count += 1
            uart.write(str(f"antal kunder {count}".encode()))
            print(count)
            if count > 10:
                led1.on()
            sleep(5)
    except Exception as e:
        print("Error reading LDR:", e)
    sleep(1)
