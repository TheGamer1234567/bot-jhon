import discord
import random
import asyncio
import os
from discord.ext import commands, tasks

# Intents necessários para ler mensagens e enviar
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Carregar as falas do arquivo
with open("falas_jhon_10000.txt", "r", encoding="utf-8") as f:
    falas = [line.strip() for line in f if line.strip()]

# Estilos de fala para variar respostas
estilos = {
    "romantico": [
        "Te amo, meu docinho 💖",
        "Você é meu anjo lindo 😘",
        "Meu amor, sempre penso em você 💕",
    ],
    "safado": [
        "Tá querendo provocar, hein? 😏",
        "Você sabe que me deixa louco(a) 🔥",
        "Quero sentir seu calor logo 😈",
    ],
    "dominador": [
        "Fica quietinho e deixa eu cuidar de você 😎",
        "Aqui quem manda sou eu, seu gostoso 😤",
        "Obedece, ou vai ver o que acontece 😏",
    ],
    "carinhoso": [
        "Vem cá, deixa eu te mimar 🥰",
        "Você é tão fofo, me derreto todo 💞",
        "Só quero te encher de dengo hoje 🥺",
    ],
}

# Dicionário dos comandos e seus gifs
commands_gifs = {
    "beijo": "https://media.giphy.com/media/KH1CTZtw1iP3W/giphy.gif",
    "carinho": "https://media.giphy.com/media/l0HlNQ03J5JxX6lva/giphy.gif",
    "abraco": "https://media.giphy.com/media/143v0Z4767T15e/giphy.gif",
    "elogio": "https://media.giphy.com/media/l0ExncehJzexFpRHq/giphy.gif",
    "provoca": "https://media.giphy.com/media/3oKIPwoeGErMmaI43C/giphy.gif",
    "dengo": "https://media.giphy.com/media/XreQmk7ETCak0/giphy.gif",
    "chama": "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
    "manda": "https://media.giphy.com/media/xT5LMHxhOfscxPfIfm/giphy.gif",
    "saudade": "https://media.giphy.com/media/l3V0lsGtTMSB5YNgc/giphy.gif",
    "mimo": "https://media.giphy.com/media/l0MYB8Ory7Hqefo9a/giphy.gif",
}

# Função para pegar fala aleatória com estilo
def get_fala_estilo(estilo=None):
    if estilo and estilo in estilos:
        return random.choice(estilos[estilo])
    return random.choice(falas)

# Tarefa que envia mensagem automática a cada 4 horas no canal 'geral'
@tasks.loop(hours=4)
async def enviar_mensagem_auto():
    canal = discord.utils.get(bot.get_all_channels(), name="geral")
    if canal:
        msg = get_fala_estilo()
        await canal.send(msg)

@bot.event
async def on_ready():
    print(f"{bot.user} conectado e pronto!")
    enviar_mensagem_auto.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Processa comandos normais do discord.ext.commands
    await bot.process_commands(message)

    # Responde mensagens que têm palavras-chave do RP
    palavras_rp = ["amor", "fofo", "lindo", "beijo", "querer", "saudade", "gostoso", "bebê", "dengo", "mimo", "carinho", "quero"]
    if any(palavra in message.content.lower() for palavra in palavras_rp):
        # Responde só se não for comando
        if not message.content.startswith("!"):
            estilo = random.choice(list(estilos.keys()))
            resposta = get_fala_estilo(estilo)
            await message.channel.send(resposta)

# Criando comandos para interações específicas
@bot.command(name="beijar")
async def cmd_beijar(ctx):
    gif = commands_gifs.get("beijo")
    frase = get_fala_estilo("romantico")
    await ctx.send(frase)
    await ctx.send(gif)

@bot.command(name="carinho")
async def cmd_carinho(ctx):
    gif = commands_gifs.get("carinho")
    frase = get_fala_estilo("carinhoso")
    await ctx.send(frase)
    await ctx.send(gif)

@bot.command(name="abracar")
async def cmd_abracar(ctx):
    gif = commands_gifs.get("abraco")
    frase = get_fala_estilo("carinhoso")
    await ctx.send(frase)
    await ctx.send(gif)

@bot.command(name="elogiar")
async def cmd_elogiar(ctx):
    gif = commands_gifs.get("elogio")
    frase = get_fala_estilo("romantico")
    await ctx.send(frase)
    await ctx.send(gif)

@bot.command(name="provocar")
async def cmd_provocar(ctx):
    gif = commands_gifs.get("provoca")
    frase = get_fala_estilo("safado")
    await ctx.send(frase)
    await ctx.send(gif)

@bot.command(name="dengo")
async def cmd_dengo(ctx):
    gif = commands_gifs.get("dengo")
    frase = get_fala_estilo("carinhoso")
    await ctx.send(frase)
    await ctx.send(gif)

@bot.command(name="chamar")
async def cmd_chamar(ctx):
    gif = commands_gifs.get("chama")
    frase = get_fala_estilo("dominador")
    await ctx.send(frase)
    await ctx.send(gif)

@bot.command(name="mandar")
async def cmd_mandar(ctx):
    gif = commands_gifs.get("manda")
    frase = get_fala_estilo("dominador")
    await ctx.send(frase)
    await ctx.send(gif)

@bot.command(name="sentir")
async def cmd_sentir(ctx):
    gif = commands_gifs.get("saudade")
    frase = get_fala_estilo("romantico")
    await ctx.send(frase)
    await ctx.send(gif)

@bot.command(name="mimar")
async def cmd_mimar(ctx):
    gif = commands_gifs.get("mimo")
    frase = get_fala_estilo("carinhoso")
    await ctx.send(frase)
    await ctx.send(gif)

# Rodar o bot
token = os.getenv("DISCORD_TOKEN")
bot.run(token)
