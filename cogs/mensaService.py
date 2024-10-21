import logging
from datetime import datetime, time

from discord import ApplicationContext
from discord.ext import commands, tasks
import discord

from models.mensa.mensaModels import Meal
from models.mensa.mensaView import MensaView
from utils import mensaUtils
from utils.constants import Constants


class MensaService(commands.Cog):
    """
    A Discord Cog for managing Mensa-related commands and tasks.
    """

    def __init__(self, bot: discord.Bot, logger: logging.Logger) -> None:
        self.bot = bot
        self.logger = logger

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        self.send_daily_mensa_message.start()

        self.logger.info("MensaService started successfully")

    @tasks.loop(time=time(hour=7, minute=0, tzinfo=Constants.SYSTIMEZONE))
    async def send_daily_mensa_message(self):
        guild: discord.Guild = self.bot.get_guild(Constants.SERVER_IDS.CUR_SERVER)
        channel: discord.TextChannel = guild.get_channel(Constants.CHANNEL_IDS.MENSA_CHANNEL)

        current_date: datetime = datetime.now()
        meals: list[Meal] = mensaUtils.get_mensa_plan(current_date)

        await channel.send(
            f"## Mensaplan vom {current_date.strftime('%d.%m.%Y')} \n ({current_date.strftime('%A')})",
            embeds=[meal.create_embed() for meal in meals])

        self.logger.info("Sent daily Mensa message")

    @commands.slash_command(
        name='mensa',
        description="Sieh dir die heutige Mensa-Auswahl an",
        guild_ids=[Constants.SERVER_IDS.CUR_SERVER])
    async def get_mensa_plan(
        self,
        ctx: ApplicationContext,
        date: discord.Option(
            str,
            "Datum",
            required=False,
            autocomplete=discord.utils.basic_autocomplete(mensaUtils.mensa_day_autocomplete))):
        if date is None:
            current_date: datetime = datetime.now()
        else:
            current_date: datetime = datetime.strptime(date, "%d.%m.%Y")
            if not mensaUtils.check_if_mensa_is_open(current_date):
                current_date = mensaUtils.get_next_mensa_day(current_date)

        meals: list[Meal] = mensaUtils.get_mensa_plan(current_date)
        await ctx.respond(
            f"## Mensaplan vom {current_date.strftime('%d.%m.%Y')} \n ({current_date.strftime('%A')})",
            embeds=[meal.create_embed() for meal in meals],
            view=MensaView(current_date))


def setup(bot: discord.Bot):
    logger = logging.getLogger("bot")
    bot.add_cog(MensaService(bot, logger))
