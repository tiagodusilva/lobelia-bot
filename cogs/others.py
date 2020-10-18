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
        await ctx.send(f"You rolled {random.randrange(1, sides)}!")
        pass

# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(OthersCog(bot))
