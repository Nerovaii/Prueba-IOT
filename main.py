# Importamos libreria para obtener fecha y hora
import datetime as dt
import time as tm

# 1.1 Importamos el package del sensor de humedad (antes temperatura)
from sensores import sensor_humedad # De sensor_temperatura a sensor_humedad

# 1.2 Importamos el package del actuador
from actuadores import rele

# 1.3 Importamos registro persistente
from registro_persistente import registro_log

# 1.4 Importamos modulo de visualizacion
import visualizacion

# Umbral de Humedad (si es menor a 60%, se activa el riego)
UMBRAL_HUMEDAD = 60

fecha_hora_actual = dt.datetime.now() # Obtenemos hora y fecha del sistema

contador_ciclos = 0

while True:

    tm.sleep(2) # Ejecución cada 2 segundos
    contador_ciclos += 1
    fecha_hora_actual = dt.datetime.now() # Obtenemos hora y fecha del sistema
    # CAMBIO: Llamamos a la nueva función del sensor de humedad
    estado_humedad = sensor_humedad.sensor_humedad() 
    
    # CAMBIO: La condición es ahora si la humedad es MENOR al umbral
    if estado_humedad < UMBRAL_HUMEDAD: 
        # Activamos el interruptor para el riego (True = ENCENDIDO)
        rele.manipular_actuador_interruptor(True)

        # CAMBIO: Mensaje para Riego ENCENDIDO con Humedad
        salida_info = f"[{fecha_hora_actual}] Evento: Riego ENCENDIDO (Humedad = {estado_humedad}%)"
        registro_log.crear_registro(str(salida_info))
        print(f"Evento: Riego ENCENDIDO (Humedad = {estado_humedad}%) con fecha y hora actual: {fecha_hora_actual}")

    else:
        # Apagamos el interruptor para el riego (False = APAGADO)
        rele.manipular_actuador_interruptor(False)

        # CAMBIO: Mensaje para Riego APAGADO con Humedad
        salida_info = f"[{fecha_hora_actual}] Evento: Riego APAGADO (Humedad = {estado_humedad}%)"
        registro_log.crear_registro(str(salida_info))
        print(f"Evento: Riego APAGADO (Humedad = {estado_humedad}%) con fecha y hora actual: {fecha_hora_actual}")

    # Generar grafico cada 10 ciclos (aprox 20 segundos)
    if contador_ciclos % 10 == 0:
        print("Generando gráfico actualizado...")
        visualizacion.generar_grafico()