# 🎵 RecordTool - Grabador de Audio Interno

Script de Python para grabar el audio interno del sistema Windows (lo que escuchas en tu computadora) con *procesamiento de audio profesional*.

## ✨ Características Principales

- 🎚️ *Procesamiento de audio profesional* con efectos de estudio
- 📀 *Grabación en formato PCM 24-bit* (calidad superior a CD)
- 🎛️ *Compresión dinámica* para equilibrar niveles de volumen
- 🔊 *Filtrado de ruido* subsónico y protección contra distorsión
- 🎯 *Detección automática de pausas* para separar archivos
- 🎤 *Soporte multi-dispositivo* de audio

## 📋 Requisitos Previos

- Python 3.7 o superior
- Windows 10/11
- Tarjeta de sonido con soporte para "Stereo Mix" o "Mezcla estéreo"

## 🚀 Instalación

### 1. Crear un ambiente virtual

Abre PowerShell o Command Prompt en la carpeta del proyecto y ejecuta:

bash
# Crear el ambiente virtual
python -m venv venv


### 2. Activar el ambiente virtual

*En PowerShell:*
powershell
.\venv\Scripts\Activate


*En Command Prompt (CMD):*
cmd
venv\Scripts\activate


> ⚠️ *Nota*: Si PowerShell bloquea la ejecución, ejecuta primero:
> powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> 

### 3. Instalar dependencias

Con el ambiente virtual activado:

bash
pip install -r requirements.txt


O instalar manualmente:

bash
pip install soundcard numpy soundfile pedalboard


### Dependencias instaladas:

- *soundcard*: Captura de audio del sistema
- *numpy*: Procesamiento numérico de señales
- *soundfile*: Lectura/escritura de audio de alta calidad
- *pedalboard*: Efectos de audio profesionales (por Spotify)

## ▶️ Ejecutar el Programa

Con el ambiente virtual activado:

bash
python Recordtool.py


## 🎯 Uso

El programa te mostrará un menú con las siguientes opciones:

1. *Listar y seleccionar dispositivo de audio*: Muestra todos los dispositivos y permite elegir cuál usar
2. *Grabar audio interno (10 segundos)*: Grabación rápida de 10 segundos
3. *Grabar audio interno (duración personalizada)*: Especifica la duración
4. *Grabar con detección automática de pausas* 🆕: Grabación continua inteligente
5. *Salir*: Cerrar el programa

### Modo 1: Seleccionar Dispositivo de Audio 🎚️

Antes de grabar, puedes seleccionar qué dispositivo de audio usar:


Selecciona una opción (1-5): 1

=== DISPOSITIVOS DE SALIDA (Speakers) ===
0: Speakers (Realtek High Definition Audio)

=== DISPOSITIVOS DE ENTRADA (Microphones) ===
0: Microphone Array (Intel)

=== LOOPBACK DEVICES (Para grabar audio interno) ===
0: Speakers (Realtek High Definition Audio) [LOOPBACK]
1: Headphones (USB Audio Device) [LOOPBACK]

Selecciona el dispositivo loopback (0-1): 1
✅ Dispositivo seleccionado: Headphones (USB Audio Device)


Una vez seleccionado, el menú mostrará qué dispositivo está activo:


📌 Dispositivo actual: Headphones (USB Audio Device)


*Notas:*
- Si solo hay un dispositivo loopback, se selecciona automáticamente
- La selección se mantiene activa para todas las grabaciones posteriores
- Puedes cambiar el dispositivo en cualquier momento volviendo a la opción 1
- Si no seleccionas ninguno, el programa usará el primer dispositivo disponible

### Modo 4: Grabación con Detección Automática de Pausas 🎯

Esta es la característica más avanzada del programa. Permite grabar sesiones largas de audio y *divide automáticamente* las grabaciones cuando detecta pausas:

#### ¿Cómo funciona?

- 🎙️ Graba *continuamente* hasta que presiones Ctrl+C
- 🔍 Detecta automáticamente cuando hay *silencio* (pausas)
- 💾 Cuando detecta una pausa de 1 segundo (configurable), *guarda el archivo automáticamente*
- 🔄 *Reanuda la grabación* automáticamente cuando detecta nuevo audio
- 📊 Muestra información *cada 2 segundos*: duración, nivel de audio (RMS), archivos guardados
- 🚀 *Optimizado* para evitar pérdidas de datos durante grabaciones largas

#### Casos de uso ideales:

- 🎵 Grabar listas de reproducción de música (separará cada canción)
- 🎙️ Podcasts o conferencias con pausas
- 🎮 Gameplays con momentos de silencio
- 📺 Videos o streams con pausas naturales

#### Ejemplo de uso:


Selecciona una opción (1-5): 4

⚙️  Configuración de detección de pausas
💡 Tip: Valores más bajos = Mayor sensibilidad
Duración de pausa para separar archivos (segundos) [default: 1.0]: 1
Umbral de silencio (0.001-0.01) [default: 0.003]: 0.003

🎤 Usando dispositivo: Speakers (Realtek High Definition Audio) [LOOPBACK]
🔍 Detectando pausas de 1.0 segundos
🎚️  Umbral de silencio: 0.3%

⚠️  Presiona Ctrl+C para detener la grabación

============================================================
🔴 Grabación iniciada...

🎵 Nuevo audio detectado - Iniciando grabación parte 1...
⏺️  Grabando... 45.2s | RMS: 0.0234
⏸️  Pausa detectada (2.1s) - Guardando archivo 1...
   ✅ grabacion_20260113_143022_parte001.wav
   📏 Tamaño: 1834.56 KB | Duración: 45.2s
   📁 C:\Users\...\grabacion_20260113_143022_parte001.wav

🔴 Esperando nuevo audio...

🎵 Nuevo audio detectado - Iniciando grabación parte 2...
⏺️  Grabando... 38.7s | RMS: 0.0198


Presiona Ctrl+C cuando termines y guardará automáticamente el último archivo.

#### Parámetros configurables:

- *Duración de pausa*: Cuántos segundos de silencio deben pasar para considerar una pausa (default: 1.0s)
  - Valor más bajo = Detecta pausas más rápido
  - Valor más alto = Menos falsos positivos
- *Umbral de silencio*: Qué tan bajo debe ser el volumen para considerarse silencio (default: 0.003 = 0.3%)
  - Valores más bajos (0.001-0.002): *Máxima sensibilidad*, detecta silencios muy sutiles
  - Valores medios (0.003-0.005): *Sensibilidad alta* (recomendado), ideal para música
  - Valores altos (0.006-0.01): *Sensibilidad moderada*, requiere pausas más evidentes

> 💡 *Tip*: Los valores por defecto están optimizados para separar canciones en una lista de reproducción. Si grabas podcasts o conferencias con mucho ruido de fondo, aumenta el umbral a 0.005 o 0.008.

### Otros modos de grabación:

#### Modo 2: Grabación simple (10 segundos)


Selecciona una opción (1-5): 2


Grabación rápida de 10 segundos. Formato: grabacion_interna_YYYYMMDD_HHMMSS.wav

#### Modo 3: Grabación con duración personalizada


Selecciona una opción (1-5): 3
Duración en segundos: 30


Especifica exactamente cuántos segundos quieres grabar.

## 🔧 Solución de Problemas

### Error: "No se encontró dispositivo loopback"

Necesitas habilitar "Stereo Mix" o "Mezcla estéreo":

1. Click derecho en el ícono de volumen (barra de tareas)
2. Selecciona *"Sonidos"* o *"Configuración de sonido"*
3. Ve a la pestaña *"Grabación"*
4. Click derecho en el espacio vacío y marca *"Mostrar dispositivos deshabilitados"*
5. Click derecho en *"Mezcla estéreo"* o *"Stereo Mix"*
6. Selecciona *"Habilitar"*

### El ambiente virtual no se activa en PowerShell

Ejecuta este comando y luego intenta activar nuevamente:

powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser


### Error al instalar dependencias

Asegúrate de tener pip actualizado:

bash
python -m pip install --upgrade pip


## 🛑 Desactivar el Ambiente Virtual

Cuando termines de usar el programa:

bash
deactivate


## 📁 Estructura del Proyecto


RecordTool/
│
├── Recordtool.py       # Script principal
├── requirements.txt    # Dependencias del proyecto
├── README.md          # Este archivo
└── venv/              # Ambiente virtual (creado después de instalación)


## 📝 Notas

- Las grabaciones se guardan en la misma carpeta donde se ejecuta el script
- El formato de salida es WAV sin comprimir
- La calidad de audio es de 44100 Hz (calidad CD)
- *Formato PCM 24-bit* para mayor rango dinámico
- El programa aplica *procesamiento de audio profesional*:
  - *HighpassFilter*: Elimina ruido subsónico (<20Hz)
  - *Compressor*: Compresión dinámica (ratio 4:1, umbral -16dB)
  - *Gain*: Amplificación de +3dB
  - *Limiter*: Protección contra distorsión (umbral -1dB)

### Formatos de archivo:

- *Modo simple*: grabacion_interna_YYYYMMDD_HHMMSS.wav
- *Modo con detección de pausas*: grabacion_YYYYMMDD_HHMMSS_parteXXX.wav
  - Cada archivo representa un segmento de audio entre pausas
  - Los números de parte son secuenciales (001, 002, 003...)

### Consideraciones técnicas:

- El modo de detección de pausas analiza el audio en *chunks de 0.5 segundos* (optimizado para evitar pérdida de datos)
- Usa *RMS (Root Mean Square)* para calcular el nivel de volumen
- Los archivos se guardan *inmediatamente* cuando se detecta una pausa (no al final)
- No hay límite de tiempo para la grabación continua
- Los warnings de discontinuidad están *suprimidos automáticamente* para una experiencia más limpia
- *Procesamiento en tiempo real* con pedalboard (tecnología de Spotify)
- *PCM 24-bit*: 144 dB de rango dinámico vs 96 dB del 16-bit
- Cada archivo se procesa automáticamente antes de guardarse

## 🤝 Contribuciones

Si encuentras algún problema o tienes sugerencias, siéntete libre de reportarlo.

---

*Desarrollado con Python 🐍*