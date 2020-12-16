from utils import monkey_patch, Context, AutoShardedBot, Bot
from discord.ext import commands

monkey_patch()


def test_context():
    assert id(Context) == id(commands.Context)


def test_bot():
    assert id(Bot) == id(commands.Bot)


def test_autoshardedbot():
    assert id(AutoShardedBot) == id(commands.AutoShardedBot)
