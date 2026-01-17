# 🎵 RecordTool - Grabador de Audio Interno

Script de Python para grabar el audio interno del sistema Windows (lo que escuchas en tu computadora).

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

### 3. I…
[12:30 a.m., 17/1/2026] Raul Castillo Luna: # 🎵 RecordTool - Grabador de Audio Interno

Script de Python para grabar el audio interno del sistema Windows (lo que escuchas en tu computadora).

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
pip install soundcard numpy scipy


## ▶️ Ejecutar el Programa

Con el ambiente virtual activado:

bash
python Recordtool.py


## 🎯 Uso

El programa te mostrará un menú con las siguientes opciones:

1. *Listar dispositivos de audio*: Muestra todos los dispositivos disponibles
2. *Grabar audio interno (10 segundos)*: Grabación rápida de 10 segundos
3. *Grabar audio interno (duración personalizada)*: Especifica la duración
4. *Salir*: Cerrar el programa

### Ejemplo de uso:


¿Qué deseas hacer?
1. Listar dispositivos de audio
2. Grabar audio interno (10 segundos)
3. Grabar audio interno (duración personalizada)
4. Salir

Selecciona una opción (1-4): 2


Las grabaciones se guardan automáticamente con el formato: grabacion_interna_YYYYMMDD_HHMMSS.wav

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
- El programa normaliza automáticamente el audio para evitar distorsión

## 🤝 Contribuciones

Si encuentras algún problema o tienes sugerencias, siéntete libre de reportarlo.

---

*Desarrollado con Python 🐍*