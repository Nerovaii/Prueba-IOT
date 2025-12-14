# Importamos el módulo random para ver la humedad
import random
import time

# Se crea una función para leer la humedad (antes temperatura)
def sensor_humedad():
    # Inicializamos la última lectura si no existe (simulando variable estática)
    if not hasattr(sensor_humedad, "ultima_lectura"):
        sensor_humedad.ultima_lectura = random.randint(40, 80)

    # Variación aleatoria pequeña (Random Walk) entre -5 y +5
    variacion = random.randint(-10, 10)
    nueva_lectura = sensor_humedad.ultima_lectura + variacion

    # Mantenemos los valores dentro de un rango realista (20% - 95%)
    nueva_lectura = max(20, min(95, nueva_lectura))
    
    # Actualizamos el estado
    sensor_humedad.ultima_lectura = nueva_lectura

    # Lectura de 2 segundos según el requerimiento
    time.sleep(2)

    return nueva_lectura