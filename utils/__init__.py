import logging

from discord.ext import commands

from utils.context import Context
from utils.bot import Bot, AutoShardedBot


logging.getLogger("utils").addHandler(logging.NullHandler())


def monkey_patch():
    logging.info("MonkeyPatch: Context")
    commands.Context = Context
    logging.info("MonkeyPatch: Bot")
    commands.Bot = Bot
    logging.info("MonkeyPatch: AutoShardedBot")
    commands.AutoShardedBot = AutoShardedBot
