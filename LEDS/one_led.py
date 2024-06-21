import Jetson.GPIO as GPIO
import time 
 
# Definimos el pin a utilizar
led_pin = 7
 
GPIO.setmode(GPIO.BOARD)  # Se establece que se va utilizar la numeració fisica de los pines
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.HIGH) # se establece que el led sera de salida, y comenzara en estado ON

#Con CTRL+C cerrarmos el programa
print("Press CTRL+C when you want the LED to stop blinking") 
 
# Bluce que parpadea el LED, mientras el time sea mas pequeño, mas rapido parpadera el LED
while True: 
  time.sleep(2) 
  GPIO.output(led_pin, GPIO.HIGH) 
  print("LED is ON")
  time.sleep(2) 
  GPIO.output(led_pin, GPIO.LOW)
  print("LED is OFF")