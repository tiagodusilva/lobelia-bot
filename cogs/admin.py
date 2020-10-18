import discord
from discord.ext import commands

import cogs.utils.bot_macros as macros
from cogs.utils.db_interactor import DbInteractor as DB

class AdminCog(commands.Cog, name="Admin"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def addTeam(self, ctx, roleName):

        """Add a team to the server:
        -> Creates role (if it doesn't exist)
        -> Adds role to internal database
        -> Creates team channels and sets their permissions"""

        if (not ctx.author.guild_permissions.administrator):
            await ctx.send(macros.FORBIDDEN_EMOTE + " Only admins can use this command")
            return

        createdRole = False
        message = ""

        # Find/Create Role
        role = discord.utils.get(ctx.guild.roles, name=roleName)
        if (role != None):
            message += f"Warning: Role for team {roleName} already exists\n"
        else:
            try:
                role = await ctx.guild.create_role(name=roleName, hoist=True, mentionable=True)
                createdRole = True
                message += f"Created role for team {roleName}\n"
            except:
                message += f"Failed to create role for team {roleName}: Aborting"
                await ctx.send(message)
                return

        # Add team to database
        if (createdRole):
            try:
                DB.replaceRole(ctx.guild.id, role.id, role.name)
            except:
                message += "Problem in database: Aborting"
                await ctx.send(message)
                return        

        # Create channels and set their permissions
        if (discord.utils.get(ctx.guild.voice_channels, name=f"team-{roleName}")):
            message += f"Warning: Category for team {roleName} already exists\n"
        else:
            try:
                category = await ctx.guild.create_category_channel("team-" + roleName)
                textChannel = await category.create_text_channel("team-" + roleName)
                voiceChannel = await category.create_voice_channel("team-" + roleName)

                message += f"Created channels for team {roleName}\n"
            except:
                message += "Failed to create channels: Aborting"
                await ctx.send(message)
                return
            
            try:
                await textChannel.set_permissions(ctx.guild.default_role, view_channel=False)
                await textChannel.set_permissions(role, view_channel=True, send_messages=True, manage_messages=True, read_messages=True)
                await voiceChannel.set_permissions(role, view_channel=True, send_messages=True, read_messages=True, connect=True)

                message += f"Set channel permissions for team {roleName}\n"
            except:
                message += "Failed to set channel permissions: Aborting"
                await ctx.send(message)
                return
        
        await ctx.send(message.rstrip('\n'))


    @commands.command(aliases=['roleReact'])
    @commands.guild_only()
    async def roleReaction(self, ctx, role: discord.Role):

        """Sends a message to assign teams based on reacts
        The bot will send a message and anyone who reacts to it will get assigned/unassigned to the corresponding team
        If a user attempts to join multiple teams, will get unassigned from the previous one
        This command is admin only"""

        if (not ctx.author.guild_permissions.administrator):
            await ctx.send(macros.FORBIDDEN_EMOTE + " Only admins can use this command")
            return

        message = await ctx.send(f"To enter team {role.mention} use the {macros.REACT_EMOTE} react below!\nWarning: Joining another team will get you unassigned from the previous one")
        await message.add_reaction(macros.REACT_EMOTE)

        try:
            DB.addRoleReaction(ctx.guild.id, message.id, ctx.channel.id, role.id)
        except:
            await message.delete()
            return


    @commands.command()
    @commands.guild_only()
    async def disableRoleReactions(self, ctx):

        """Disables all previous role reaction messages.
        From this point onwards old messages will be edited to say they are no longer valid
        This command is admin only"""

        if (not ctx.author.guild_permissions.administrator):
            await ctx.send(macros.FORBIDDEN_EMOTE + " Only admins can use this command")
            return

        messages = None
        try:
            messages = DB.get_message_react_pairs(ctx.guild.id)
        except:
            ctx.send("Couldn't retrive database pairs: Aborting")
            return

        try:
            DB.deleteGuildRoleReactions(ctx.guild.id)
        except:
            await ctx.send("Failed to commit database transaction: Aborting")
            return

        for p in messages:
            message = await (ctx.guild.get_channel(p[1])).fetch_message(p[0])
            await message.edit(content=message.content + "\nThis message has been deactivated, reacts will have no more effect from now on")

        await ctx.send("All previous messages are now invalid")



# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(AdminCog(bot))
