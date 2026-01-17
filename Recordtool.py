"""
Script para grabar el audio interno del sistema Windows
Requiere: pip install soundcard numpy scipy
"""

import soundcard as sc
import numpy as np
from scipy.io import wavfile
from datetime import datetime
import os

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
    for i, device in enumerate(loopbacks):
        if device.isloopback:
            print(f"{i}: {device.name} [LOOPBACK]")

def grabar_audio_interno(duracion_segundos=10, frecuencia_muestreo=44100):
    """
    Graba el audio interno del sistema
    
    Args:
        duracion_segundos: Duración de la grabación en segundos
        frecuencia_muestreo: Frecuencia de muestreo (Hz)
    """
    try:
        # Obtener el dispositivo loopback por defecto
        # Esto graba el audio que está sonando en tu computadora
        mics = sc.all_microphones(include_loopback=True)
        loopback_device = None
        
        for mic in mics:
            if mic.isloopback:
                loopback_device = mic
                break
        
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
        data = np.array(data)
        
        # Si es estéreo, mantener ambos canales
        if len(data.shape) > 1:
            print(f"📊 Grabación estéreo: {data.shape}")
        else:
            print(f"📊 Grabación mono: {data.shape}")
        
        # Normalizar y convertir a int16
        data = data / np.max(np.abs(data))  # Normalizar
        data = (data * 32767).astype(np.int16)
        
        # Generar nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"grabacion_interna_{timestamp}.wav"
        
        # Guardar archivo WAV
        wavfile.write(nombre_archivo, frecuencia_muestreo, data)
        
        ruta_completa = os.path.abspath(nombre_archivo)
        print(f"\n✅ Grabación completada!")
        print(f"📁 Archivo guardado: {ruta_completa}")
        print(f"📏 Tamaño: {os.path.getsize(nombre_archivo) / 1024:.2f} KB")
        
    except Exception as e:
        print(f"\n❌ Error durante la grabación: {str(e)}")
        print("\n💡 Asegúrate de tener instaladas las dependencias:")
        print("   pip install soundcard numpy scipy")

def main():
    print("=" * 60)
    print("  🎵 GRABADOR DE AUDIO INTERNO - WINDOWS")
    print("=" * 60)
    
    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Listar dispositivos de audio")
        print("2. Grabar audio interno (10 segundos)")
        print("3. Grabar audio interno (duración personalizada)")
        print("4. Salir")
        
        opcion = input("\nSelecciona una opción (1-4): ").strip()
        
        if opcion == "1":
            listar_dispositivos()
        
        elif opcion == "2":
            grabar_audio_interno(duracion_segundos=10)
        
        elif opcion == "3":
            try:
                duracion = int(input("Duración en segundos: "))
                if duracion > 0:
                    grabar_audio_interno(duracion_segundos=duracion)
                else:
                    print("❌ La duración debe ser mayor a 0")
            except ValueError:
                print("❌ Por favor ingresa un número válido")
        
        elif opcion == "4":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    main()