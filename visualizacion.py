import matplotlib.pyplot as plt
import datetime as dt
import re
import os

def generar_grafico():
    datos_por_semana = {} # Key: "YYYY-WW", Value: {'fechas': [], 'humedades': [], 'temperaturas': []}
    
    archivo_log = 'registro_bodega.txt'
    carpeta_salida = 'imagenes_analisis'
    
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    
    try:
        with open(archivo_log, 'r') as f:
            for linea in f:
                # Intenta coincidir con el nuevo formato: Humedad=XX%, Temp=XX°C
                # [2025-12-14 17:45:50.287496] Evento: Riego ENCENDIDO (MEDIA POTENCIA) (Humedad=58%, Temp=30°C)
                match_nuevo = re.search(r'\[(.*?)\].*Humedad=(\d+)%, Temp=(\d+)°C', linea)
                
                # Intenta coincidir con el formato antiguo (si es necesario para compatibilidad, aunque el usuario reinició)
                # [2025-12-14 15:44:37.136833] Evento: Riego ENCENDIDO (Humedad = 32%)
                match_antiguo = re.search(r'\[(.*?)\].*Humedad = (\d+)%', linea)
                
                fecha = None
                humedad = None
                temp = None

                if match_nuevo:
                    fecha_str = match_nuevo.group(1)
                    humedad = int(match_nuevo.group(2))
                    temp = int(match_nuevo.group(3))
                elif match_antiguo:
                    # Si es formato antiguo, no tenemos temperatura. Podemos ignorarlo o poner None.
                    # Para este caso, ignoraremos datos antiguos para no mezclar gráficos con/sin temperatura.
                    continue 

                if fecha and humedad is not None:
                    pass # Ya tenemos los datos
                elif match_nuevo:
                     # Parsear fecha
                    try:
                        fecha = dt.datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S.%f')
                    except ValueError:
                        continue
                else:
                    continue

                # Agrupar por semana
                year, week, _ = fecha.isocalendar()
                clave_semana = f"{year}_{week}"
                
                if clave_semana not in datos_por_semana:
                    datos_por_semana[clave_semana] = {'fechas': [], 'humedades': [], 'temperaturas': []}
                
                datos_por_semana[clave_semana]['fechas'].append(fecha)
                datos_por_semana[clave_semana]['humedades'].append(humedad)
                datos_por_semana[clave_semana]['temperaturas'].append(temp)

        if not datos_por_semana:
            print("No se encontraron datos válidos para graficar.")
            return

        for semana, datos in datos_por_semana.items():
            fig, ax1 = plt.subplots(figsize=(10, 6))

            # Eje 1: Humedad (Azul)
            color = 'tab:blue'
            ax1.set_xlabel('Fecha y Hora')
            ax1.set_ylabel('Humedad (%)', color=color)
            ax1.plot(datos['fechas'], datos['humedades'], color=color, marker='o', markersize=4, label='Humedad')
            ax1.tick_params(axis='y', labelcolor=color)
            ax1.grid(True)

            # Eje 2: Temperatura (Rojo)
            ax2 = ax1.twinx()  
            color = 'tab:red'
            ax2.set_ylabel('Temperatura (°C)', color=color)  
            ax2.plot(datos['fechas'], datos['temperaturas'], color=color, marker='x', linestyle='--', markersize=4, label='Temperatura')
            ax2.tick_params(axis='y', labelcolor=color)

            plt.title(f'Historial de Humedad y Temperatura - Semana {semana}')
            fig.tight_layout()  
            
            nombre_archivo = f"reporte_semana_{semana}.png"
            ruta_completa = os.path.join(carpeta_salida, nombre_archivo)
            plt.savefig(ruta_completa)
            plt.close() 
            print(f"Gráfico guardado: {ruta_completa}")

    except FileNotFoundError:
        print(f"El archivo {archivo_log} no existe.")

if __name__ == "__main__":
    generar_grafico()
