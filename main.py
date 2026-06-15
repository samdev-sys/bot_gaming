import os
import logging
from pathlib import Path
from dotenv import load_dotenv  # type: ignore[import]
import discord  # type: ignore[import]
from discord.ext import commands  # type: ignore[import]

# Configuración profesional de logs para producción
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('bot_moderacion')

# Asegurar la carga del .env en la ruta absoluta correcta
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv('DISCORD_TOKEN')

# Validación preventiva del TOKEN
if not TOKEN:
    raise ValueError("Error: No se encontró el DISCORD_TOKEN en el archivo .env")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('------')
    print(f'Moderador listo: {bot.user.name} (ID: {bot.user.id})')
    print('------')
    logger.info(f'Bot conectado exitosamente como {bot.user}')

# 1. Limpiar chat (Optimizado y Seguro)
@bot.command()
@commands.has_permissions(manage_messages=True)
@commands.bot_has_permissions(manage_messages=True)
async def limpiar(ctx, cantidad: int):
    """Borra una cantidad de mensajes especificada (Máximo 100)"""
    if cantidad <= 0:
        return await ctx.send("Por favor, introduce un número mayor a 0.", delete_after=3)
    
    # Límite preventivo para evitar bloqueos de la API de Discord
    if cantidad > 100:
        return await ctx.send("⚠️ Por razones de estabilidad, solo puedes borrar hasta 100 mensajes a la vez.", delete_after=5)
    
    # Se suma 1 para incluir el comando del usuario en la limpieza
    await ctx.channel.purge(limit=cantidad + 1)
    await ctx.send(f'🧹 {cantidad} mensajes han sido eliminados por {ctx.author.mention}', delete_after=5)

# 2. Expulsar (Validación doble de permisos)
@bot.command()
@commands.has_permissions(kick_members=True)
@commands.bot_has_permissions(kick_members=True)
async def expulsar(ctx, member: discord.Member, *, razon=None):
    """Expulsa a un miembro del servidor"""
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("No puedes expulsar a alguien con un rol igual o superior al tuyo.")
        
    await member.kick(reason=razon)
    await ctx.send(f'👢 {member.mention} ha sido expulsado por {ctx.author.mention}. Razón: {razon if razon else "No especificada"}')

# 3. Banear (Validación doble de permisos)
@bot.command()
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def banear(ctx, member: discord.Member, *, razon=None):
    """Banea a un miembro del servidor"""
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("No puedes banear a alguien con un rol igual o superior al tuyo.")

    await member.ban(reason=razon)
    await ctx.send(f'🔨 {member.mention} ha sido baneado por {ctx.author.mention}. Razón: {razon if razon else "No especificada"}')

# 4. Manejo avanzado de errores
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'⚠️ Lo siento {ctx.author.mention}, no tienes permisos para usar este comando.')
    elif isinstance(error, commands.BotMissingPermissions):
        permisos_faltantes = ", ".join(error.missing_permissions)
        await ctx.send(f'❌ El bot no puede ejecutar esta acción porque le faltan los siguientes permisos en el servidor: `{permisos_faltantes}`')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'ℹ️ Por favor, proporciona todos los argumentos necesarios. Uso correcto: `{ctx.command.signature}`')
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'❌ Argumento inválido. Asegúrate de mencionar a un usuario válido o usar un número correcto.')
    else:
        # Registro detallado del error en el sistema de logs en lugar de un print básico
        logger.error(f'Error no controlado en el comando {ctx.command}:', exc_info=error)
        await ctx.send(f'Ocurrió un error inesperado al ejecutar el comando.')

bot.run(TOKEN)