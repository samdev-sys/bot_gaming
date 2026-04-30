import os
from dotenv import load_dotenv  # type: ignore[import]
import discord  # type: ignore[import]
from discord.ext import commands  # type: ignore[import]

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot =commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'moderador listo  {bot.user.name} ')
    print('------')
#limpiar chat
@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpiar(ctx ,cantidad: int):
    """borra una cantidad de mensajes especificada"""
    await ctx.channel.purge(limit=cantidad)
    await ctx.send(f'{cantidad} mensajes han sido eliminados por {ctx.author.mention}', delete_after=5)
#expulsar
@bot.command()
@commands.has_permissions(kick_members=True)
async def expulsar(ctx, member: discord.Member, *, razon=None):
    """expulsa a un miembro del servidor"""
    await member.kick(reason=razon)
    await ctx.send(f'{member.mention} ha sido expulsado por {ctx.author.mention}. Razón: {razon}')
#banear
@bot.command()
@commands.has_permissions(ban_members=True)
async def banear(ctx, member: discord.Member, *, razon=None):
    """banea a un miembro del servidor"""
    await member.ban(reason=razon)
    await ctx.send(f'{member.mention} ha sido baneado por {ctx.author.mention}. Razón: {razon}')

#manejo de errores
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'Lo siento {ctx.author.mention}, no tienes permisos para usar este comando.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Por favor, proporciona todos los argumentos necesarios para este comando, {ctx.author.mention}.')
    else:
        await ctx.send(f'Ocurrió un error al ejecutar el comando: {error}')

bot.run(TOKEN)