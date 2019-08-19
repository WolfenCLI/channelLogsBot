from discord.ext import commands
import discord
import os
import re

prefix = "?"
MESSAGESLIMIT = None
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


def isDayTopic(message: discord.Message):
    return message.pinned and re.search(r"day \d:", message.content, re.MULTILINE | re.IGNORECASE)


@bot.command()
async def dump(ctx):
    author: discord.Member = ctx.author
    channel: discord.TextChannel = ctx.message.channel
    fileName = "{}.md".format(channel.name)

    if author.bot:
        return

    if not is_admin(author):
        await ctx.send("Admin only feature")
        return

    history = []
    async for message in channel.history(limit=MESSAGESLIMIT):
        history.insert(0, message)
    # history is already in order, from 0 to number_of_messages

    f = open(fileName, "w+", encoding="utf-8")
    currPos = 0
    while currPos < (len(history) - 1):
        currAuthor: discord.Member = history[currPos].author

        f.writelines(u"#### {}\n".format(currAuthor.name))
        for message in history[currPos:]:
            if message.content == "?dump":
                currPos += 1
            elif message.author == currAuthor:
                if isDayTopic(message):
                    f.writelines(u"# {}  \n".format(history[currPos].content))
                    currPos += 1
                    continue

                f.writelines(message.content + "  \n")

                if len(message.attachments) > 0:
                    for attachment in message.attachments:
                        f.writelines("- Attachment: {}  \n".format(attachment.url))

                currPos += 1
            else:
                break
    f.close()
    await ctx.send("Here's your dump", file=discord.File(fileName))
    os.remove(fileName)
