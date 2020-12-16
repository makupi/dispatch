# dpy-utils


from utils import monkey_patch, Context
from discord.ext import commands

import unittest


class MonkeyPatchTest(unittest.TestCase):
    def setUp(self):
        monkey_patch()

    def test_context(self):
        self.assertEqual(id(commands.Context), id(Context))
