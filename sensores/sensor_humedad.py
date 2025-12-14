# Importamos el módulo random para ver la humedad
import random
import time

# Se crea una función para leer la humedad (antes temperatura)
def sensor_humedad(temperatura_ambiente, potencia_riego):
    # Inicializamos la última lectura si no existe (simulando variable estática)
    if not hasattr(sensor_humedad, "ultima_lectura"):
        sensor_humedad.ultima_lectura = random.randint(40, 80)

    # 1. Factor de secado (Drying)
    # A mayor temperatura, mayor secado.
    # Base de secado: 1%
    # Si temp > 25, aumenta el secado.
    factor_secado = 1 + max(0, (temperatura_ambiente - 25) * 0.2)
    
    # 2. Factor de riego (Wetting)
    # Depende de la potencia del riego (0-100)
    # Si potencia es 100, sube aprox 5-8%. Si es 50, sube 2-4%.
    factor_riego = 0
    if potencia_riego > 0:
        factor_riego = (potencia_riego / 100) * random.uniform(4, 8)

    # Variación neta
    variacion = factor_riego - factor_secado
    
    # Añadimos un poco de ruido aleatorio (-1 a +1)
    variacion += random.uniform(-1, 1)

    nueva_lectura = sensor_humedad.ultima_lectura + variacion

    # Mantenemos los valores dentro de un rango realista (10% - 100%)
    nueva_lectura = max(10, min(100, nueva_lectura))
    
    # Actualizamos el estado
    sensor_humedad.ultima_lectura = nueva_lectura

    # Lectura de 2 segundos según el requerimiento
    time.sleep(2)

    return int(nueva_lectura)