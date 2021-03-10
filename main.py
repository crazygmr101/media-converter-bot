import os

import discord
import dotenv
from discord.ext import commands
from random import randint
import traceback

bot = commands.Bot(help_command=None, command_prefix="!!")
dotenv.load_dotenv()


@bot.event
async def on_ready():
    print(f"Ready as {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    if message.author.id != 569362627935862784:
        return
    if not message.attachments:
        return

    # get message attachment type
    typ = message.attachments[0].filename.split(".")[-1]

    if message.attachments[0].size > 8000000:
        return

    if typ not in ["mkv", "avi"]:
        return

    filename = "".join(map(str, (randint(0, 10) for s in range(10))))

    try:
        with open(f"/tmp/{filename}.{typ}", "wb") as fp:
            await message.attachments[0].save(fp)

        await message.add_reaction("🔄")

        if typ == 'mkv':
            os.system(f"ffmpeg -i /tmp/{filename}.{typ} -codec copy /tmp/{filename}.mp4")
        else:
            os.system(f"ffmpeg -i /tmp/{filename}.{typ} /tmp/{filename}.mp4")

        with open(f"/tmp/{filename}.mp4", "rb") as fp:
            file: discord.File = discord.File(fp)
            channel: discord.TextChannel = message.channel

            await channel.send(f"Media converted from {message.jump_url} - Sent by {message.author.mention}",
                               file=file,
                               allowed_mentions=discord.AllowedMentions.none())

        await message.remove_reaction("🔄", bot.user)
    except Exception as e:  # noqa
        print(traceback.print_tb(e.__traceback__))

    os.remove(f"/tmp/{filename}.{typ}")
    os.remove(f"/tmp/{filename}.mp4")




bot.run(os.getenv("TOKEN"))
