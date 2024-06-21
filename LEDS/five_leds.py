import Jetson.GPIO as GPIO
import time

#Los pines siempre empiezan en estado ON, lo que significa una vez conectado el circuito los 5 LEDs estran encendidos a la vez.
# Configuración de los pines GPIO
led_pins = [18, 23, 24, 12, 16]  #Ponemos los pines que vamos a utilizar

GPIO.setmode(GPIO.BOARD)  # Se establece que se va utilizar la numeració fisica de los pines
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT) # Se define los pines de salida, ya que los leds se controlan como salida 

# Función para crear el efecto de barrido de los LEDs
def fantastic_car_effect(iterations, delay):
    for _ in range(iterations):
        # Barrido hacia la derecha
        for pin in led_pins:
            GPIO.output(pin, GPIO.HIGH)# Pines en estado ON
            time.sleep(delay)
            GPIO.output(pin, GPIO.LOW) # Pines en estado OFF

        # Barrido hacia la izquierda
        for pin in reversed(led_pins):
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(pin, GPIO.LOW)

try:
    iterations = 10  # Número de veces que se repite el efecto, en total 20 iteraciones de ida y vuelta
    delay = 0.15  # Duración de encendido de cada LED en segundos, mientras mas pequeño este retardo mas rapidosera la transicion de los leds
    fantastic_car_effect(iterations, delay) #Ejecutmos la función
finally:
    GPIO.cleanup()  # Restablece la configuración de los pines GPIO