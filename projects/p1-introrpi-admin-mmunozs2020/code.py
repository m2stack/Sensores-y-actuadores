import RPi.GPIO as GPIO

# inicializamos la board y el pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

# objeto pwm para regular la potencia segun su frecuencia
pwm = GPIO.PWM(11, 100) #--> frecuencia = 100Hz

print("INICIO DEL CODIGO EFECTIVO")

#1# - encendiendo el led al 100% de su brillo máximo (100% del DutyCycle)
pwm.start(100)
input("Pulse cualquier tecla para continuar")

#2# - cambiamos el DutyCycle al 50% para que luzca la mitad
pwm.ChangeDutyCycle(50)
input("Pulse de nuevo para proseguir")

#3# - por último, DutyCycle al 1% para probar un brillo muy tenue
pwm.ChangeDutyCycle(1)
input("Vuelva a pulsar para terminar")

# desactivamos pwm y limpiamos lo pertinente a GPIO
pwm.stop()
GPIO.cleanup()