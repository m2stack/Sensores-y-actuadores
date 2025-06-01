#!/usr/bin/env python3
import sys, tty, termios, time, pigpio

PIN_SERVO         = 2 # numeracion en modo BCM (que es el usado por defecto por pigpio)

# direcciones de movimiento
ADELANTE          = "w"
PARADA            = "x"
ATRAS             = "s"


def leerOrden(): # para leer orden por teclado a comandar al motor
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)

  try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)

  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

'''
  Según especificaciones de la compañía fabricante de estos servos, Parallax,
  la modulación PWM de estos servos tiene los siguientes rangos:
  - Girar en un sentido: [1280...1480]
  - Parar: 1500
  - Girar en el otro: [1520...1720]

  Mientras más cerca al valor 1500, más despacio; cuanto más alejado, más rápido.
'''

# gira en un sentido a la velocidad determinada por la marcha que recibe
def adelante (marcha):
  print("> [w][%.d] adelante" % marcha)
  velocidad = 1520 + 40 * marcha
  miServo.set_servo_pulsewidth(PIN_SERVO, velocidad)

# gira en reversa(^) a la velocidad determinada por la marcha que recibe
def atras (marcha):
  print("> [s][%.d] atras" % marcha)
  velocidad = 1480 - 40 * marcha
  miServo.set_servo_pulsewidth(PIN_SERVO, velocidad)

# detiene el giro en cualquier sentido y para el servo
def parar ():
  print("> [x][->1] parando motor...")
  miServo.set_servo_pulsewidth(PIN_SERVO, 1500) # 1.º lo ponemos a 0 rpm
  time.sleep(1)
  miServo.set_servo_pulsewidth(PIN_SERVO, 0) # y 2.º lo "apagamos"
  miServo.stop()
  print("- motor parado")
  
  # en cuanto se pare el motor, terminamos el programa
  global motor_on
  motor_on = False
  return
  
#-- funciones nuevas:

# Recibe direccion y marcha y establece el movimiento y velocidad debidos
def control_motor(direccion, marcha):
  if direccion == ADELANTE:
    adelante(marcha)
    
  elif direccion == ATRAS:
    atras(marcha)
  
  elif direccion == PARADA:
    marcha = 1
    parar()
  
  return direccion, marcha

# Recibe la direccion previa y una marcha nueva. Cambia la marcha
def control_por_orden(orden, midir, mimar):
  ndir, nmar = midir, mimar
  
  if orden in "wsx":
    ndir, nmar = control_motor(orden, mimar)
    
  elif orden in "012345":
    ndir, nmar = control_motor(midir, int(orden))
    
  return ndir, nmar

#==========================================================================

# (setup inicial)
miServo = pigpio.pi() # instancia de la clase pi de la libreria pigpio
                      # Usaremos el demonio pigpiod para comandar al motor por teclado
                      # Por ello, IMPORTANTE, hay que lanzar el demonio: sudo pigpiod
mi_direccion  = ADELANTE
mi_marcha     = 1      # empieza en la primera marcha (como un coche)
motor_on      = True

print ("Dispositivo listo. Esperando órdenes\n\
[DIRECCIONES]: [w = adelante, s = atrás, x = parar]\n\
[VELOCIDADES][0 = parada en direccion X; 1,2,3,4,5 = marchas incrementales]")

while motor_on:
  orden = leerOrden()
  
  # modificamos el estado del motor y guardamos su marcha y direccion
  # tras recibir cada orden nueva hasta detectar una parada
  mi_direccion, mi_marcha = control_por_orden(orden, mi_direccion, mi_marcha)
