# Variable estado actuador rele o interruptor apagado

estado_rele = False

# Función que enciende y apaga el actuador (Riego).
def manipular_actuador_interruptor(accion_en_actuador):
    if accion_en_actuador == True:
        # ENCENDIDO
        estado_rele = True

    elif accion_en_actuador == False:
        # APAGADO
        estado_rele = False

    return estado_rele