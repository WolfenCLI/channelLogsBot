from discord.ext import commands
import discord

prefix = "?"
MESSAGESLIMIT = 1000
bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    print("Everything's all ready to go~")


@bot.command()
async def ping(ctx):
    latency = bot.latency
    await ctx.send(latency)


def is_admin(author: discord.Member):
    return author.guild_permissions.administrator


@bot.command()
async def dump(ctx):
    author: discord.Member = ctx.author
    channel: discord.TextChannel = ctx.message.channel
    if not is_admin(author):
        ctx.send("Admin only feature")
        return
    async for message in channel.history(limit=MESSAGESLIMIT):
        print(message)
