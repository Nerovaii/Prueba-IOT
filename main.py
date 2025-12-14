# Importamos libreria para obtener fecha y hora
import datetime as dt
import time as tm

# 1.1 Importamos el package del sensor de humedad (antes temperatura)
from sensores import sensor_humedad # De sensor_temperatura a sensor_humedad
# 1.1.2 Importamos sensor de temperatura ambiente
from sensores import sensor_temperatura_ambiente

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
potencia_riego = 0 # 0 = Apagado, 0-100 = Potencia

while True:

    tm.sleep(1) # Ejecución cada 1 segundo
    contador_ciclos += 1
    fecha_hora_actual = dt.datetime.now() # Obtenemos hora y fecha del sistema
    
    # 1. Leemos temperatura ambiente
    temp_ambiente = sensor_temperatura_ambiente.sensor_temperatura()
    
    # 2. Leemos humedad (pasando temp y potencia actual)
    estado_humedad = sensor_humedad.sensor_humedad(temp_ambiente, potencia_riego)
    
    # 3. Lógica de control
    if estado_humedad < UMBRAL_HUMEDAD:
        # Necesitamos regar. Decidimos la potencia.
        # Si hace mucho calor (> 30) o está muy seco (< 40), potencia máxima.
        if temp_ambiente > 30 or estado_humedad < 40:
            nueva_potencia = 100
            tipo_riego = "ALTA POTENCIA"
        else:
            nueva_potencia = 50
            tipo_riego = "MEDIA POTENCIA"
            
        # Activamos actuador
        rele.manipular_actuador_interruptor(nueva_potencia)
        potencia_riego = nueva_potencia

        # Mensaje
        salida_info = f"[{fecha_hora_actual}] Evento: Riego ENCENDIDO ({tipo_riego}) (Humedad={estado_humedad}%, Temp={temp_ambiente}°C)"
        registro_log.crear_registro(str(salida_info))
        print(f"Evento: Riego ENCENDIDO ({tipo_riego}) (Humedad={estado_humedad}%, Temp={temp_ambiente}°C) con fecha y hora actual: {fecha_hora_actual}")

    else:
        # Apagamos
        rele.manipular_actuador_interruptor(0)
        potencia_riego = 0

        # Mensaje
        salida_info = f"[{fecha_hora_actual}] Evento: Riego APAGADO (Humedad={estado_humedad}%, Temp={temp_ambiente}°C)"
        registro_log.crear_registro(str(salida_info))
        print(f"Evento: Riego APAGADO (Humedad={estado_humedad}%, Temp={temp_ambiente}°C) con fecha y hora actual: {fecha_hora_actual}")

    # Generar grafico cada 10 ciclos (aprox 20 segundos)
    if contador_ciclos % 10 == 0:
        print("Generando gráfico actualizado...")
        visualizacion.generar_grafico()