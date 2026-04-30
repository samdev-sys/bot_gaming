# Discord Moderation Bot

Bot de moderación para Discord construido con `discord.py`.

## Descripción

Este bot proporciona comandos básicos de moderación para un servidor de Discord, incluyendo:

- `!limpiar <cantidad>`: elimina mensajes recientes del canal.
- `!expulsar @miembro [razón]`: expulsa a un miembro del servidor.
- `!banear @miembro [razón]`: banea a un miembro del servidor.

Además incluye manejo básico de errores para permisos faltantes y argumentos requeridos.

## Requisitos

- Python 3.8 o superior
- Biblioteca `discord.py`
- Biblioteca `python-dotenv`

## Instalación

1. Clona el repositorio o descarga el proyecto.
2. En la carpeta del proyecto, crea un entorno virtual opcional:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Instala las dependencias:

```powershell
pip install -r requirements.txt
```

Si no tienes un `requirements.txt`, puedes instalar directamente:

```powershell
pip install discord.py python-dotenv
```

## Configuración

Crea un archivo `.env` en la raíz del proyecto con el token de tu bot de Discord:

```env
DISCORD_TOKEN=tu_token_aqui
```

## Uso

Ejecuta el bot desde la raíz del proyecto:

```powershell
python main.py
```

Cuando el bot se conecte, verás un mensaje en consola indicando que está listo.

### Comandos disponibles

- `!limpiar <cantidad>`
  - Requiere permiso: `manage_messages`
  - Elimina la cantidad de mensajes indicada del canal actual.

- `!expulsar @miembro [razón]`
  - Requiere permiso: `kick_members`
  - Expulsa al miembro mencionado.

- `!banear @miembro [razón]`
  - Requiere permiso: `ban_members`
  - Banea al miembro mencionado.

## Permisos necesarios del bot

Asegúrate de que el bot tenga permisos adecuados en tu servidor para:

- Leer mensajes y ver canales
- Enviar mensajes
- Administrar mensajes (`manage_messages`)
- Expulsar miembros (`kick_members`)
- Banear miembros (`ban_members`)

## Manejo de errores

El bot envía mensajes cuando:

- El usuario no tiene permisos para ejecutar un comando.
- Falta algún argumento obligatorio del comando.
- Ocurre otro error inesperado en la ejecución del comando.

## Notas adicionales

- El bot usa `discord.Intents.default()` y habilita explícitamente `message_content` y `members`.
- Ajusta la configuración de intents en el portal de desarrolladores de Discord si tu bot necesita acceder al contenido de mensajes y a los miembros.
