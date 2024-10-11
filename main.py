import logging
import os
import typing
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

import discord.ext.commands
from discord.ext import commands

from utils.constants import Constants


def get_extensions() -> typing.List[str]:
    files = Path("cogs").rglob("*.py")
    for file in files:
        yield file.as_posix()[:-3].replace("/", ".")


def load_extensions(bot: commands.Bot, extensions: typing.List[str]):
    for ext_file in extensions:
        try:
            bot.load_extension(ext_file)
            print(f"Loaded {ext_file}")
        except Exception as ex:
            print(f"Failed to load {ext_file}: {ex}")


def unload_extensions(bot: commands.Bot, extensions: typing.List[str]):
    for ext_file in extensions:
        try:
            bot.unload_extension(ext_file)
            print(f"Unloaded {ext_file}")
        except Exception as ex:
            print(f"Failed to unload {ext_file}: {ex}")


def main():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='discord.log',
                                  encoding='utf-8',
                                  mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix="$",
                       intents=intents,
                       case_insensitive=True,
                       help_command=None,
                       description="A cool bot that does cool things")

    load_dotenv()

    @bot.event
    async def on_ready():
        print('---------------------------')
        print(datetime.now())
        print('Logged in as:')
        print(bot.user.name)
        print(bot.user.id)
        print('---------------------------')

    @bot.command(name="reload")
    @commands.has_permissions(manage_webhooks=True)
    async def reload(ctx: commands.Context):
        unload_extensions(bot, get_extensions())
        load_extensions(bot, get_extensions())
        await ctx.send("Done")

    @bot.command(name="shutdown")
    @commands.has_permissions(manage_webhooks=True)
    async def shutdown(ctx):
        await ctx.message.add_reaction(Constants.REACTIONS.CHECK)
        print("########################################################\n"
              "########################SHUTDOWN########################\n"
              f"Der Bot wurde von {ctx.author} heruntergefahren.\n"
              "########################SHUTDOWN########################\n"
              "########################################################\n")
        await bot.close()

    load_extensions(bot, get_extensions())
    bot.run(str(os.getenv("DISCORD_TOKEN")))


if __name__ == "__main__":
    main()
