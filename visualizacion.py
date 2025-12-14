import matplotlib.pyplot as plt
import datetime as dt
import re
import os

def generar_grafico():
    datos_por_semana = {} # Key: "YYYY-WW", Value: {'fechas': [], 'humedades': []}
    
    archivo_log = 'registro_bodega.txt'
    carpeta_salida = 'imagenes_analisis'
    
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    
    try:
        with open(archivo_log, 'r') as f:
            for linea in f:
                # Formato esperado: [2025-12-14 15:44:37.136833] Evento: Riego ENCENDIDO (Humedad = 32%)
                match = re.search(r'\[(.*?)\].*Humedad = (\d+)%', linea)
                if match:
                    fecha_str = match.group(1)
                    humedad_str = match.group(2)
                    
                    try:
                        fecha = dt.datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S.%f')
                        humedad = int(humedad_str)
                        
                        # Get ISO year and week
                        year, week, _ = fecha.isocalendar()
                        clave_semana = f"{year}_{week}"
                        
                        if clave_semana not in datos_por_semana:
                            datos_por_semana[clave_semana] = {'fechas': [], 'humedades': []}
                        
                        datos_por_semana[clave_semana]['fechas'].append(fecha)
                        datos_por_semana[clave_semana]['humedades'].append(humedad)
                        
                    except ValueError:
                        print(f"Error al parsear fecha: {fecha_str}")
                        continue

        if not datos_por_semana:
            print("No se encontraron datos válidos para graficar.")
            return

        for semana, datos in datos_por_semana.items():
            plt.figure(figsize=(10, 6))
            plt.plot(datos['fechas'], datos['humedades'], marker='o', linestyle='-', color='b', markersize=4)
            
            plt.title(f'Historial de Humedad - Semana {semana}')
            plt.xlabel('Fecha y Hora')
            plt.ylabel('Humedad (%)')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            nombre_archivo = f"reporte_semana_{semana}.png"
            ruta_completa = os.path.join(carpeta_salida, nombre_archivo)
            plt.savefig(ruta_completa)
            plt.close() # Close to free memory
            print(f"Gráfico guardado: {ruta_completa}")

    except FileNotFoundError:
        print(f"El archivo {archivo_log} no existe.")

if __name__ == "__main__":
    generar_grafico()
