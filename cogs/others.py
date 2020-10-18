import cogs.utils.bot_macros as macros

import random

import discord
from discord.ext import commands

class OthersCog(commands.Cog, name="Other"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['commandlist', 'commands', 'h'], hidden=True)
    async def _help(self, ctx):
        await ctx.send_help()

    @commands.command(aliases=["d"])
    async def dice(self, ctx, sides :int):
        """Throws an N sided dice"""
        if (sides < 1):
            return

        await ctx.send(f"You rolled {random.randrange(1, sides + 1)}!")
        pass

    @commands.command()
    async def info(self, ctx):
        """Info about the bot"""
        await ctx.send("""This bot is open source and its code can be found in the following repository:
        https://github.com/tiagodusilva/XtremeBot""")

# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(OthersCog(bot))
