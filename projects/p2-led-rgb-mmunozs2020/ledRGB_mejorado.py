# ledRGB.py
# Practica 2. Sensores y actuadores. URJC. Julio Vega

import time, sys
import RPi.GPIO as GPIO

FREQ_PWM = 100

pin_rojo  = 11
pin_azul  = 13
pin_verde = 15

# lista de colores modificada
# las tuplas contienen los valores (RGB) que se necesita aplicar como pwm
lista_colores = {
	"rojo": (100, 0, 0),
	"azul": (0, 0, 100),
	"verde": (0, 100, 0),
	"amarillo": (100, 100, 0),
	"naranja": (100, 50, 0),
	"magenta": (100, 0, 100),
	"cian": (0, 100, 100),
	"morado": (50, 0, 50)
}


#-- DECLARACION DE FUNCIONES A UTILIZAR :

# ahora las funciones de encender y apagar toman de parametro una tupla
def encender(tupla_pwm):
	
	r, g, b = tupla_pwm
	
	if not(r==0): pwm_rojo.ChangeDutyCycle(FREQ_PWM - r)
	if not(g==0): pwm_verde.ChangeDutyCycle(FREQ_PWM - g)
	if not(b==0): pwm_azul.ChangeDutyCycle(FREQ_PWM - b)
	
def apagar(tupla_pwm):
	
	r, g, b = tupla_pwm
	
	if not(r==0): pwm_rojo.ChangeDutyCycle(r)
	if not(g==0): pwm_verde.ChangeDutyCycle(g)
	if not(b==0):  pwm_azul.ChangeDutyCycle(b)
    
def apagar_todo():
	
	pwm_rojo.ChangeDutyCycle(FREQ_PWM)
	pwm_verde.ChangeDutyCycle(FREQ_PWM)
	pwm_azul.ChangeDutyCycle(FREQ_PWM)
	
#-- CODIGO SECUENCIAL :

# comenzamos con todos los pines configurados y apagados
GPIO.setmode(GPIO.BOARD)

for pin in (pin_rojo, pin_azul, pin_verde):
	
	GPIO.setup(pin, GPIO.OUT)

# establecemos modulacion pwm para los tres pines pertinentes del led
pwm_rojo  = GPIO.PWM(pin_rojo, FREQ_PWM)
pwm_azul  = GPIO.PWM(pin_azul, FREQ_PWM)
pwm_verde = GPIO.PWM(pin_verde, FREQ_PWM)

# establecemos un dutyCycle inicial al maximo de frecuencia por la
# polaridad invertida
for pwm in (pwm_rojo, pwm_azul, pwm_verde):
	
	pwm.start(FREQ_PWM)
	

#-- CODIGO ITERATIVO :

while True:
	
	#Imprimimos un mensaje por terminal para que el usuario elija el LED
	print("Por favor, ingrese una orden válida para el LED: ")
	print("[encender + color | apagar + color | terminar]")
	
	proto_orden = input("- ")
	
	# Terminamos el programa si se introduce la palabra terminar
	if(proto_orden == "terminar"):
		
		codigo_de_color = (0, 0, 0)
		encender(codigo_de_color)
		
		break
		
	orden = proto_orden.split()
	
	# comprobamos que sea una orden valida
	if len(orden) == 2:
		
		accion, color = orden
		
		# determinamos si la accion es encender o apagar
		if(accion == "encender") and color in lista_colores:
			
			codigo_de_color = lista_colores[color]
			encender(codigo_de_color)

		elif(accion == "apagar"):
			
			if color in lista_colores:
				
				codigo_de_color = lista_colores[color]
				apagar(codigo_de_color)
			
			# si se ha introducido 'apagar todo' como entrada
			# se restablecen los dutycycle, apagando asi el led
			elif color == "todo":
				
				apagar_todo()
		
		print("HECHO!")
		print()
			
	# Ante cualquier entrada no prevista, avisamos del error
	else:
		print("ERR: color no válido")
		print()
    

GPIO.cleanup()
