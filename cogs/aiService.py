import logging

from discord import ApplicationContext
from discord.ext import commands, tasks
import discord

from models.database.userData import User
from utils.ai import ai
from utils.memeUtils import memeUtils
from utils.constants import Constants


class AIService(commands.Cog):
    """
    A Discord Cog for using the OpenAI API to translate code.
    """

    def __init__(self, bot: discord.Bot, logger: logging.Logger) -> None:
        self.logger = logger
        self.bot = bot

        self.ai = ai.AIUtils()

    @commands.slash_command(
        name="translate",
        description="Übersetze den gegebenen Code in die angegebene Sprache.",
        guild_ids=[Constants.SERVER_IDS.CUR_SERVER]
    )
    @discord.option(
        "language",
        type=discord.SlashCommandOptionType.string,
        required=True
    )
    @discord.option(
        "code",
        type=discord.SlashCommandOptionType.string,
        required=True
    )
    async def translate(
        self,
        ctx: ApplicationContext,
        language: str,
        code: str
    ):
        """
        Translates the given code into the specified language.
        """

        await ctx.defer()

        try:
            response = self.ai.code_translate(language, code)
        except Exception as e:
            self.logger.error(f"Error translating code: {e}")
            await ctx.respond(
                "Es gab einen Fehler beim Übersetzen des Codes.",
                ephemeral=True
            )
            return

        embed = await response.create_embed(ctx.author, 1)

        await ctx.respond(embed=embed)


def setup(bot: discord.Bot):
    logger = logging.getLogger("bot")
    bot.add_cog(AIService(bot, logger))
