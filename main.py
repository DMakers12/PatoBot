from discord.ext import commands
import keep_alive
import time
import discord
from discord_components import Button, DiscordComponents
import asyncio
import json

import os

token = os.environ['token']
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="p!", intents=intents)

DiscordComponents(bot)

@bot.command(pass_context=True)
async def hola(ctx):
  mensaje = await ctx.send("chao")
  await mensaje.edit(content="na mentira")


@bot.command(pass_context=True)
async def ping(ctx):
  antes = time.monotonic()
  mensaje = await ctx.send("Pong!")
  ping1 = (time.monotonic() - antes)*1000
  ping2 = (str(ping1).split('.'))[0]
  await mensaje.edit(content="Pong! (" + ping2 + "ms)")


@bot.command(pass_context=True)
async def embed(ctx):
  embed = discord.Embed(title="Titulo", description="Descripcion 1 2 3 4 5 6 7 8 9 10", color=0xffffff)
  embed.set_footer(text="Sub-texto")
  embed.add_field(name="Info 1", value="Hola", inline=True)
  embed.add_field(name="Info 2", value="Chao", inline=True)
  await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def imagen(ctx):
  imagen = discord.File("imagen.png", filename="imagen.png")
  await ctx.send(content="Aqui esta tu imagen", file=imagen)


@bot.command(pass_context=True)
async def mensaje(ctx, usuario:discord.Member, nick):
  mensaje = ctx.message
  await ctx.send(mensaje.author)
  await ctx.send(mensaje.author.name)
  await ctx.send(nick)
  channel = await mensaje.author.create_dm()
  await channel.send("HOLA")
  await usuario.edit(nick=nick)


@bot.command(pass_context=True)
async def boton(ctx):
  await ctx.send(
        "JIJIJIJA",
        components = [
            Button(label = "apreta para discord nitro gratis", custom_id = "boton1")
        ]
    )
  interaction = await bot.wait_for("button_click", check = lambda i: i.custom_id == "boton1")
  await interaction.send(content = "troliadisimo")


@bot.command(pass_context=True)
async def texto(ctx, *texto:str):
  texto = ' '.join(texto)
  with open('archivo.json', "r+") as f:
    archivo = json.load(f)
  archivo[str(ctx.author.name)] = str(texto)
  with open('archivo.json', "r+") as f:
    json.dump(archivo, f)
  await ctx.send("Listo!")


@bot.command(pass_context=True)
async def mandarImagen(ctx):
  while True:
    imagen = discord.File("imagen.png", filename="imagen.png")
    await ctx.send(file=imagen)
    await asyncio.sleep(120)


@bot.command(pass_context=True)
async def parar(ctx):
  await ctx.send("Apagando bot...")
  await bot.close()


@bot.event
async def on_ready():
  print(f"el bot {bot.user} ta listo")
  cantidad = 0
  for servidor in bot.guilds:
    cantidad = cantidad + len(servidor.members)
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{cantidad} usuarios"))


keep_alive.keep_alive()
bot.run(token)