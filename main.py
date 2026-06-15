import os
from dotenv import load_dotenv  # type: ignore[import]
import discord  # type: ignore[import]
from discord.ext import commands  # type: ignore[import]

load_dotenv()
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

# 1. Limpiar chat (Optimizado)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpiar(ctx, cantidad: int):
    """Borra una cantidad de mensajes especificada"""
    if cantidad <= 0:
        return await ctx.send("Por favor, introduce un número mayor a 0.", delete_after=3)
    
    # Se suma 1 para incluir el comando del usuario en la limpieza
    await ctx.channel.purge(limit=cantidad + 1)
    await ctx.send(f'🧹 {cantidad} mensajes han sido eliminados por {ctx.author.mention}', delete_after=5)

# 2. Expulsar
@bot.command()
@commands.has_permissions(kick_members=True)
async def expulsar(ctx, member: discord.Member, *, razon=None):
    """Expulsa a un miembro del servidor"""
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("No puedes expulsar a alguien con un rol igual o superior al tuyo.")
        
    await member.kick(reason=razon)
    await ctx.send(f'👢 {member.mention} ha sido expulsado por {ctx.author.mention}. Razón: {razon if razon else "No especificada"}')

# 3. Banear
@bot.command()
@commands.has_permissions(ban_members=True)
async def banear(ctx, member: discord.Member, *, razon=None):
    """Banea a un miembro del servidor"""
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("No puedes banear a alguien con un rol igual o superior al tuyo.")

    await member.ban(reason=razon)
    await ctx.send(f'🔨 {member.mention} ha sido baneado por {ctx.author.mention}. Razón: {razon if razon else "No especificada"}')

# 4. Manejo de errores (Seguro para evitar bucles en reconexiones)
@bot.event
async def on_command_error(ctx, error):
    # Ignorar comandos que no existen para no saturar el chat/consola
    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'⚠️ Lo siento {ctx.author.mention}, no tienes permisos para usar este comando.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'ℹ️ Por favor, proporciona todos los argumentos necesarios. Uso correcto: `{ctx.command.signature}`')
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'❌ Argumento inválido. Asegúrate de mencionar a un usuario válido o usar un número correcto.')
    else:
        # Esto envía el error real a la consola para que puedas auditar si el bot se cae
        print(f'Error en comando {ctx.command}: {error}')
        await ctx.send(f'Ocurrió un error inesperado al ejecutar el comando.')

bot.run(TOKEN)