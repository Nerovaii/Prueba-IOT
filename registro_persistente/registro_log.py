#Función para crear y guardar archivo log

def crear_registro(texto_evento):
#Reemplazamos true y false x Encendido y Apagado
    texto_limpio = str(texto_evento)
    texto_limpio.replace(" False " , " APAGADO ")
    texto_limpio.replace(" True " , "ENCENDIDO ")

    registro_log = open ("registro_bodega.txt", "a")
    registro_log.write(texto_limpio+" \n") #El salto de línea