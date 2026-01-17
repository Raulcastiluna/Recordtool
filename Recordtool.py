"""
Script para grabar el audio interno del sistema Windows
Requiere: pip install soundcard numpy soundfile pedalboard
"""

import soundcard as sc
import numpy as np
import soundfile as sf
from pedalboard import Pedalboard, Compressor, Gain, Limiter, HighpassFilter
from datetime import datetime
import os
import threading
import time
import warnings

def listar_dispositivos():
    """Muestra todos los dispositivos de audio disponibles"""
    print("\n=== DISPOSITIVOS DE SALIDA (Speakers) ===")
    speakers = sc.all_speakers()
    for i, speaker in enumerate(speakers):
        print(f"{i}: {speaker.name}")
    
    print("\n=== DISPOSITIVOS DE ENTRADA (Microphones) ===")
    mics = sc.all_microphones()
    for i, mic in enumerate(mics):
        print(f"{i}: {mic.name}")
    
    print("\n=== LOOPBACK DEVICES (Para grabar audio interno) ===")
    loopbacks = sc.all_microphones(include_loopback=True)
    loopback_list = []
    for i, device in enumerate(loopbacks):
        if device.isloopback:
            loopback_list.append(device)
            print(f"{len(loopback_list)-1}: {device.name} [LOOPBACK]")
    
    return loopback_list

def seleccionar_dispositivo():
    """Permite al usuario seleccionar un dispositivo loopback"""
    loopbacks = listar_dispositivos()
    
    if not loopbacks:
        print("\n❌ No se encontraron dispositivos loopback.")
        print("\n💡 SOLUCIÓN:")
        print("1. Click derecho en el ícono de volumen (barra de tareas)")
        print("2. Selecciona 'Sonidos' o 'Configuración de sonido'")
        print("3. Ve a la pestaña 'Grabación'")
        print("4. Click derecho en el espacio vacío y marca 'Mostrar dispositivos deshabilitados'")
        print("5. Habilita 'Mezcla estéreo' o 'Stereo Mix'")
        return None
    
    if len(loopbacks) == 1:
        print(f"\n✅ Usando dispositivo: {loopbacks[0].name}")
        return loopbacks[0]
    
    try:
        print("\n")
        seleccion = int(input(f"Selecciona el dispositivo loopback (0-{len(loopbacks)-1}): "))
        if 0 <= seleccion < len(loopbacks):
            print(f"✅ Dispositivo seleccionado: {loopbacks[seleccion].name}")
            return loopbacks[seleccion]
        else:
            print("❌ Selección inválida")
            return None
    except ValueError:
        print("❌ Por favor ingresa un número válido")
        return None

def obtener_dispositivo_loopback(dispositivo_seleccionado=None):
    """Obtiene el dispositivo loopback a usar"""
    if dispositivo_seleccionado is not None:
        return dispositivo_seleccionado
    
    # Buscar el primer dispositivo loopback disponible
    mics = sc.all_microphones(include_loopback=True)
    for mic in mics:
        if mic.isloopback:
            return mic
    return None

def procesar_audio(audio_data, samplerate):
    """Aplica procesamiento de audio profesional para mejorar la calidad"""
    # Crear cadena de efectos de audio profesional
    board = Pedalboard([
        HighpassFilter(cutoff_frequency_hz=20.0),  # Filtrar ruido subsónico
        Compressor(threshold_db=-16, ratio=4),     # Compresión dinámica
        Gain(gain_db=3),                            # Amplificación
        Limiter(threshold_db=-1.0)                  # Prevenir distorsión
    ])
    
    # Aplicar efectos
    audio_procesado = board(audio_data.T, samplerate)
    return audio_procesado.T

def grabar_audio_interno(duracion_segundos=10, frecuencia_muestreo=44100, dispositivo=None):
    """
    Graba el audio interno del sistema
    
    Args:
        duracion_segundos: Duración de la grabación en segundos
        frecuencia_muestreo: Frecuencia de muestreo (Hz)
        dispositivo: Dispositivo loopback a usar (None para usar el predeterminado)
    """
    try:
        # Obtener el dispositivo loopback
        loopback_device = obtener_dispositivo_loopback(dispositivo)
        
        if loopback_device is None:
            print("❌ No se encontró dispositivo loopback.")
            print("\n💡 SOLUCIÓN:")
            print("1. Click derecho en el ícono de volumen (barra de tareas)")
            print("2. Selecciona 'Sonidos' o 'Configuración de sonido'")
            print("3. Ve a la pestaña 'Grabación'")
            print("4. Click derecho en el espacio vacío y marca 'Mostrar dispositivos deshabilitados'")
            print("5. Habilita 'Mezcla estéreo' o 'Stereo Mix'")
            return
        
        print(f"\n🎤 Usando dispositivo: {loopback_device.name}")
        print(f"⏱️  Grabando durante {duracion_segundos} segundos...")
        print("▶️  Reproduciendo algo en tu computadora para capturar el audio\n")
        
        # Grabar audio
        with loopback_device.recorder(samplerate=frecuencia_muestreo) as mic:
            data = mic.record(numframes=int(frecuencia_muestreo * duracion_segundos))
        
        # Convertir a formato adecuado para guardar
        data = np.array(data, dtype=np.float32)
        
        # Si es estéreo, mantener ambos canales
        if len(data.shape) > 1:
            print(f"📊 Grabación estéreo: {data.shape}")
        else:
            print(f"📊 Grabación mono: {data.shape}")
        
        # Aplicar procesamiento de audio profesional
        print("🎛️  Aplicando procesamiento de audio...")
        data = procesar_audio(data, frecuencia_muestreo)
        
        # Generar nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"grabacion_interna_{timestamp}.wav"
        
        # Guardar archivo WAV con soundfile (mayor calidad)
        sf.write(nombre_archivo, data, frecuencia_muestreo, subtype='PCM_24')
        
        ruta_completa = os.path.abspath(nombre_archivo)
        print(f"\n✅ Grabación completada!")
        print(f"📁 Archivo guardado: {ruta_completa}")
        print(f"📏 Tamaño: {os.path.getsize(nombre_archivo) / 1024:.2f} KB")
        
    except Exception as e:
        print(f"\n❌ Error durante la grabación: {str(e)}")
        print("\n💡 Asegúrate de tener instaladas las dependencias:")
        print("   pip install soundcard numpy soundfile pedalboard")

def calcular_rms(audio_data):
    """Calcula el RMS (Root Mean Square) del audio para detectar volumen"""
    return np.sqrt(np.mean(np.square(audio_data)))

def grabar_con_deteccion_pausas(umbral_silencio=0.003, duracion_pausa=1.0, frecuencia_muestreo=44100, dispositivo=None):
    """
    Graba audio interno detectando pausas automáticamente.
    Cuando detecta una pausa de 1 segundo, guarda el archivo y comienza uno nuevo.
    
    Args:
        umbral_silencio: Nivel RMS por debajo del cual se considera silencio (0.003 = 0.3%)
        duracion_pausa: Duración del silencio en segundos para considerar una pausa
        frecuencia_muestreo: Frecuencia de muestreo (Hz)
        dispositivo: Dispositivo loopback a usar (None para usar el predeterminado)
    """
    try:
        # Obtener el dispositivo loopback
        loopback_device = obtener_dispositivo_loopback(dispositivo)
        
        if loopback_device is None:
            print("❌ No se encontró dispositivo loopback.")
            print("\n💡 SOLUCIÓN:")
            print("1. Click derecho en el ícono de volumen (barra de tareas)")
            print("2. Selecciona 'Sonidos' o 'Configuración de sonido'")
            print("3. Ve a la pestaña 'Grabación'")
            print("4. Click derecho en el espacio vacío y marca 'Mostrar dispositivos deshabilitados'")
            print("5. Habilita 'Mezcla estéreo' o 'Stereo Mix'")
            return
        
        print(f"\n🎤 Usando dispositivo: {loopback_device.name}")
        print(f"🔍 Detectando pausas de {duracion_pausa} segundos")
        print(f"🎚️  Umbral de silencio: {umbral_silencio * 100:.1f}%")
        print("\n⚠️  Presiona Ctrl+C para detener la grabación\n")
        print("=" * 60)
        
        # Variables de control
        grabando = True
        contador_archivos = 0
        buffer_audio = []
        tiempo_silencio = 0
        tamano_chunk = int(frecuencia_muestreo * 0.5)  # Chunks de 0.5 segundos (optimizado)
        en_silencio = False
        
        # Suprimir warnings de discontinuidad durante la grabación
        warnings.filterwarnings('ignore', category=sc.SoundcardRuntimeWarning)
        
        # Flag para control de threading
        stop_flag = threading.Event()
        
        def guardar_archivo(data, numero):
            """Guarda el audio en un archivo WAV con procesamiento profesional"""
            if len(data) == 0:
                return None
                
            data = np.concatenate(data, axis=0)
            data = np.array(data, dtype=np.float32)
            
            # Aplicar procesamiento de audio profesional
            data = procesar_audio(data, frecuencia_muestreo)
            
            # Generar nombre de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"grabacion_{timestamp}_parte{numero:03d}.wav"
            
            # Guardar con soundfile (mayor calidad)
            sf.write(nombre_archivo, data, frecuencia_muestreo, subtype='PCM_24')
            
            ruta_completa = os.path.abspath(nombre_archivo)
            tamano_kb = os.path.getsize(nombre_archivo) / 1024
            duracion_seg = len(data) / frecuencia_muestreo
            
            return {
                'nombre': nombre_archivo,
                'ruta': ruta_completa,
                'tamano': tamano_kb,
                'duracion': duracion_seg
            }
        
        print("🔴 Grabación iniciada...\n")
        
        with loopback_device.recorder(samplerate=frecuencia_muestreo) as mic:
            while not stop_flag.is_set():
                try:
                    # Leer chunk de audio
                    chunk = mic.record(numframes=tamano_chunk)
                    
                    # Calcular nivel de audio (RMS)
                    rms = calcular_rms(chunk)
                    
                    # Detectar si es silencio
                    if rms < umbral_silencio:
                        if not en_silencio:
                            # Comenzó el silencio
                            en_silencio = True
                            tiempo_inicio_silencio = time.time()
                        else:
                            # Continúa el silencio
                            tiempo_silencio = time.time() - tiempo_inicio_silencio
                            
                            # Si el silencio dura más de la duración especificada
                            if tiempo_silencio >= duracion_pausa and len(buffer_audio) > 0:
                                # Guardar el archivo actual
                                contador_archivos += 1
                                print(f"⏸️  Pausa detectada ({tiempo_silencio:.1f}s) - Guardando archivo {contador_archivos}...")
                                
                                info = guardar_archivo(buffer_audio, contador_archivos)
                                if info:
                                    print(f"   ✅ {info['nombre']}")
                                    print(f"   📏 Tamaño: {info['tamano']:.2f} KB | Duración: {info['duracion']:.1f}s")
                                    print(f"   📁 {info['ruta']}")
                                    print("\n🔴 Esperando nuevo audio...\n")
                                
                                # Limpiar buffer
                                buffer_audio = []
                                tiempo_silencio = 0
                    else:
                        # Hay audio
                        if en_silencio and len(buffer_audio) == 0:
                            print(f"🎵 Nuevo audio detectado - Iniciando grabación parte {contador_archivos + 1}...")
                        
                        en_silencio = False
                        tiempo_silencio = 0
                        buffer_audio.append(chunk)
                        
                        # Mostrar indicador de grabación (menos frecuente para no interrumpir)
                        if len(buffer_audio) % 4 == 0:  # Cada 2 segundos aproximadamente
                            duracion_actual = len(buffer_audio) * 0.5
                            print(f"⏺️  Grabando... {duracion_actual:.1f}s | RMS: {rms:.4f}", end='\r')
                
                except KeyboardInterrupt:
                    stop_flag.set()
                    break
        
        # Guardar el último archivo si hay audio en el buffer
        if len(buffer_audio) > 0:
            contador_archivos += 1
            print(f"\n\n💾 Guardando última grabación (archivo {contador_archivos})...")
            info = guardar_archivo(buffer_audio, contador_archivos)
            if info:
                print(f"   ✅ {info['nombre']}")
                print(f"   📏 Tamaño: {info['tamano']:.2f} KB | Duración: {info['duracion']:.1f}s")
                print(f"   📁 {info['ruta']}")
        
        print("\n" + "=" * 60)
        print(f"✅ Grabación finalizada! Total de archivos: {contador_archivos}")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Grabación detenida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la grabación: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\n💡 Asegúrate de tener instaladas las dependencias:")
        print("   pip install soundcard numpy soundfile pedalboard")

def main():
    print("=" * 60)
    print("  🎵 GRABADOR DE AUDIO INTERNO - WINDOWS")
    print("=" * 60)
    
    dispositivo_seleccionado = None  # Variable para almacenar el dispositivo seleccionado
    
    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Listar y seleccionar dispositivo de audio")
        print("2. Grabar audio interno (10 segundos)")
        print("3. Grabar audio interno (duración personalizada)")
        print("4. Grabar con detección automática de pausas 🆕")
        print("5. Salir")
        
        if dispositivo_seleccionado:
            print(f"\n📌 Dispositivo actual: {dispositivo_seleccionado.name}")
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion == "1":
            dispositivo_seleccionado = seleccionar_dispositivo()
        
        elif opcion == "2":
            grabar_audio_interno(duracion_segundos=10, dispositivo=dispositivo_seleccionado)
        
        elif opcion == "3":
            try:
                duracion = int(input("Duración en segundos: "))
                if duracion > 0:
                    grabar_audio_interno(duracion_segundos=duracion, dispositivo=dispositivo_seleccionado)
                else:
                    print("❌ La duración debe ser mayor a 0")
            except ValueError:
                print("❌ Por favor ingresa un número válido")
        
        elif opcion == "4":
            print("\n⚙️  Configuración de detección de pausas")
            print("💡 Tip: Valores más bajos = Mayor sensibilidad")
            try:
                duracion_pausa = float(input("Duración de pausa para separar archivos (segundos) [default: 1.0]: ") or "1.0")
                umbral = float(input("Umbral de silencio (0.001-0.01) [default: 0.003]: ") or "0.003")
                
                if duracion_pausa > 0 and 0 < umbral < 1:
                    grabar_con_deteccion_pausas(
                        umbral_silencio=umbral,
                        duracion_pausa=duracion_pausa,
                        dispositivo=dispositivo_seleccionado
                    )
                else:
                    print("❌ Valores inválidos")
            except ValueError:
                print("❌ Por favor ingresa números válidos")
            except KeyboardInterrupt:
                print("\n⏹️  Grabación cancelada")
        
        elif opcion == "5":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción no válida")

if __name__ == "_main_":
    main()