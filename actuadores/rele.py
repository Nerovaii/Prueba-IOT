# Variable estado actuador rele o interruptor apagado

estado_rele = False
potencia_actual = 0

# Función que enciende y apaga el actuador (Riego).
# Ahora acepta un nivel de potencia (0-100)
def manipular_actuador_interruptor(potencia):
    global estado_rele, potencia_actual
    
    # Si se pasa un booleano por compatibilidad
    if isinstance(potencia, bool):
        potencia = 100 if potencia else 0

    if potencia > 0:
        # ENCENDIDO
        estado_rele = True
        potencia_actual = potencia
    else:
        # APAGADO
        estado_rele = False
        potencia_actual = 0

    return estado_rele, potencia_actual