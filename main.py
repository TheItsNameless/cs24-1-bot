import logging
import os
import typing
from datetime import datetime
from pathlib import Path

from tortoise import Tortoise, run_async
from aerich import Command
from dotenv import load_dotenv

import discord.ext.commands
from discord.ext import commands

import tortoiseConfig
from utils.constants import Constants


def get_extensions() -> typing.List[str]:
    files = Path("cogs").rglob("*.py")
    for file in files:
        yield file.as_posix()[:-3].replace("/", ".")


def load_extensions(bot: commands.Bot, logger: logging.Logger, extensions: typing.List[str]):
    for ext_file in extensions:
        try:
            bot.load_extension(ext_file)
            logger.info("Loaded %s", ext_file)
        except Exception as ex:
            logger.error("Failed to load %s: %s", ext_file, ex)


def unload_extensions(bot: commands.Bot, logger: logging.Logger, extensions: typing.List[str]):
    for ext_file in extensions:
        try:
            bot.unload_extension(ext_file)
            logger.info("Unloaded %s", ext_file)
        except Exception as ex:
            logger.error("Failed to unload %s: %s", ext_file, ex)


def setup_discord_logger():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='discord.log',
                                  encoding='utf-8',
                                  mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


def setup_bot_logger():
    logger = logging.getLogger('bot')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='bot.log',
                                  encoding='utf-8',
                                  mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(console_handler)

async def init_database():

    # update the database
    command = Command(tortoise_config=tortoiseConfig.TORTOISE_ORM, app="models")
    await command.init()
    await command.upgrade(run_in_transaction=True)

    # init the database
    await Tortoise.init(config=tortoiseConfig.TORTOISE_ORM)
    await Tortoise.generate_schemas()


def main():
    setup_discord_logger()
    setup_bot_logger()

    run_async(init_database())

    logger = logging.getLogger("bot")

    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix="$",
                       intents=intents,
                       case_insensitive=True,
                       help_command=None,
                       description="A cool bot that does cool things")

    load_dotenv()

    @bot.event
    async def on_ready():
        logger.info(
            "Logged in as: %s (%s) on guild %s",
            bot.user.name, bot.user.id, bot.get_guild(int(Constants.SERVER_IDS.CUR_SERVER)).name)

    @bot.command(name="reload")
    @commands.has_permissions(manage_webhooks=True)
    async def reload(ctx: commands.Context):
        unload_extensions(bot, logger, get_extensions())
        load_extensions(bot, logger, get_extensions())
        await ctx.send("Done")

    @bot.command(name="shutdown")
    @commands.has_permissions(manage_webhooks=True)
    async def shutdown(ctx):
        await ctx.message.add_reaction(Constants.REACTIONS.CHECK)
        logger.info("The bot was shut down by %s", ctx.author)
        await bot.close()

    load_extensions(bot, logger, get_extensions())
    bot.run(str(os.getenv("DISCORD_TOKEN")))

    bot.user.edit()


if __name__ == "__main__":
    main()
