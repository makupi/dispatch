import logging

from discord.ext import commands

from dispatch.context import Context
from dispatch.bot import Bot, AutoShardedBot
from dispatch.settings import Settings
from dispatch.paginator import EmbedPaginator


logging.getLogger("dispatch").addHandler(logging.NullHandler())


def monkey_patch():
    logging.info("MonkeyPatch: Context")
    commands.Context = Context
    logging.info("MonkeyPatch: Bot")
    commands.Bot = Bot
    logging.info("MonkeyPatch: AutoShardedBot")
    commands.AutoShardedBot = AutoShardedBot
