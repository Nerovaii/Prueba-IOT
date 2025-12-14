import random

def sensor_temperatura():
    # Inicializamos la temperatura si no existe (simulando variable estática)
    if not hasattr(sensor_temperatura, "ultima_lectura"):
        sensor_temperatura.ultima_lectura = random.randint(20, 30)

    # Random Walk: Variación pequeña entre -1 y +1 grados
    variacion = random.choice([-1, 0, 1])
    
    # A veces hay cambios más bruscos (simulando nubes o sol directo)
    if random.random() < 0.1:
        variacion += random.choice([-2, 2])

    nueva_lectura = sensor_temperatura.ultima_lectura + variacion

    # Mantenemos los valores dentro de un rango realista (15°C - 40°C)
    nueva_lectura = max(15, min(40, nueva_lectura))
    
    # Actualizamos el estado
    sensor_temperatura.ultima_lectura = nueva_lectura

    return nueva_lectura
