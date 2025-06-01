# ledRGB.py
# Practica 2. Sensores y actuadores. URJC. Julio Vega

import time, sys
import RPi.GPIO as GPIO

pin_rojo  = 11
pin_azul  = 13
pin_verde = 15

lista_colores = {
	"1": pin_rojo,
	"2": pin_azul,
	"3": pin_verde
}

#-- DECLARACION DE FUNCIONES A UTILIZAR :

def encender(pin):
	
    GPIO.output(pin, GPIO.LOW)
    
def apagar(pin):
	
    GPIO.output(pin, GPIO.HIGH)
    
#-- CODIGO SECUENCIAL :

# comenzamos con todos los pines configurados y apagados
GPIO.setmode(GPIO.BOARD)
	
for pin in (pin_rojo, pin_azul, pin_verde):
	
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

#-- CODIGO ITERATIVO :

while True:
	
	#Imprimimos un mensaje por terminal para que el usuario elija el LED
	print("Por favor, ingrese un color válido para el LED: ")
	print("[1: rojo		2: azul		3: verde	0: salir]")
	
	num = input("- ")
	
	# Comprobamos 
	if(num in lista_colores):
		
		encender(lista_colores[num])
		
		# Se apagará el led seleccionado al pulsar cualquier otra tecla
		input("Pulse cualquier tecla para apagar")
		apagar(lista_colores[num])
		
	# Terminamos el programa si se introduce un 0
	elif(num == "0"):
		
		break
		
	# Ante cualquier entrada no prevista, avisamos del error
	else:
		print("ERR: color no válido")
    

GPIO.cleanup()    
