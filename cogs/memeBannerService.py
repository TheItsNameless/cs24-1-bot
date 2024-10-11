import logging
from datetime import datetime, time

from discord import ApplicationContext
from discord.ext import commands, tasks
import discord

from models.mensa.mensaModels import Meal
from models.mensa.mensaView import MensaView
from utils import mensaUtils, memeBannerUtils
from utils.constants import Constants


class MemeBannerService(commands.Cog):
    """
    A Discord Cog for getting memes and changing the bots banner.
    """

    def __init__(self, bot: discord.Bot, logger: logging.Logger) -> None:
        self.logger = logger
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Starts the set_random_meme_banner task when the bot is ready.
        """
        self.set_random_meme_banner.start()

        self.logger.info("MemeBannerService started successfully")

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        """
        Listens for messages in the meme channel and saves them as memes.
        """
        if message.author.bot:
            return

        if str(message.channel.id) == Constants.CHANNEL_IDS.MEME_CHANNEL:
            for attachment in message.attachments:
                if attachment.content_type.startswith("image"):
                    await memeBannerUtils.save_meme_image(attachment)

                    self.logger.info("Saved meme %s from %s", attachment.filename, message.author)

    @tasks.loop(minutes=5)
    async def set_random_meme_banner(self):
        random_meme = memeBannerUtils.get_random_meme_image()

        try:
            await self.bot.user.edit(banner=random_meme)
            self.logger.info("Successfully set random meme banner")
        except discord.HTTPException as ex:
            self.logger.error("Failed to set random meme banner %s", ex)


def setup(bot: discord.Bot):
    logger = logging.getLogger("bot")
    bot.add_cog(MemeBannerService(bot, logger))
