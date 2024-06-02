import espnow
from ili934xnew import ILI9341, color565
from machine import Pin, SPI, ADC
import m5stack
import tt14
import glcdfont
import tt14
import tt32
import network
from time import sleep

fonts = [glcdfont,tt14,tt24,tt32]

text = 'Tryk på knap efter tilfredshed.'

power = Pin(m5stack.TFT_LED_PIN, Pin.OUT)
power.value(1)

spi = SPI(
    2,
    baudrate=40000000,
    miso=Pin(m5stack.TFT_MISO_PIN),
    mosi=Pin(m5stack.TFT_MOSI_PIN),
    sck=Pin(m5stack.TFT_CLK_PIN))

display = ILI9341(
    spi,
    cs=Pin(m5stack.TFT_CS_PIN),
    dc=Pin(m5stack.TFT_DC_PIN),
    rst=Pin(m5stack.TFT_RST_PIN),
    w=320,
    h=240,
    r=3)

display.erase()
display.set_pos(0,0)
for ff in fonts:
    display.set_font(ff)
    display.print(text)

station = network.WLAN(network.STA_IF) 
station.active(True)

esp_now = espnow.ESPNow()
esp_now.active(True)
peer = b'\xB0\xA7\x32\xDD\x70\x08'  
esp_now.add_peer(peer)


adc_pin = ADC(Pin(26))
adc_pin.atten(ADC.ATTN_11DB)

pb1 = 0
pb2 = 0
pb3 = 0
pb = Pin(16, Pin.IN)

while True:
    adc_value = adc_pin.read()
    if adc_value > 2600 and adc_value < 2800:
        print("knap 1 trykket")
        pb1 += 1
        msg = f"7c 1"
        esp_now.send(peer, msg)
    elif adc_value > 1800 and adc_value < 2000:
        print("knap 2 trykket")
        pb2 += 1
        msg = f"7c 2"
        esp_now.send(peer, msg)
    elif pb.value() == 1:
        print("knap 3 trykket")
        pb3 += 1
        msg = f"7c 3"
        esp_now.send(peer, msg)
    sleep(3)





