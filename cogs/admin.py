import discord
from discord.ext import commands

import cogs.utils.botMacros as macros
from cogs.utils.dbInterface import DbInterface as DB

class AdminCog(commands.Cog, name="Admin"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def addTeam(self, ctx, roleName):

        """Add a team to the server
        -> Creates role (if it doesn't exist)
        -> Adds role to internal database
        -> Creates team channels and sets their permissions"""

        if (not ctx.author.guild_permissions.administrator):
            await ctx.send(macros.FORBIDDEN_EMOTE + " Only admins can use this command")
            return

        message = ""
        roleName = f"Team {roleName}"

        # Find/Create Role
        existingTeam = DB.get_team_from_name(ctx.guild.id, roleName)
        if (existingTeam != None):
            message += f"{roleName} already exists in database: Aborting"
            await ctx.send(message)
            return

        role = discord.utils.get(ctx.guild.roles, name=roleName)
        if (role != None):
            message += f"Warning: Role for {roleName} already exists\n"
        else:
            try:
                role = await ctx.guild.create_role(name=roleName, hoist=True, mentionable=True, reason=f"{ctx.author.display_name} ran the addTeam command")
                message += f"Created role for {roleName}\n"
            except:
                message += f"Failed to create role for {roleName}: Aborting"
                await ctx.send(message)
                return

        category, textChannel, voiceChannel = None, None, None
        # Create channels and set their permissions
        if (discord.utils.get(ctx.guild.voice_channels, name=roleName)):
            message += f"Warning: Channels for {roleName} may already exist\n"
        else:
            try:
                category = await ctx.guild.create_category_channel(roleName)
                textChannel = await category.create_text_channel(roleName)
                voiceChannel = await category.create_voice_channel(roleName)

                message += f"Created channels for {roleName}\n"
            except:
                message += "Failed to create channels: Aborting"
                await ctx.send(message)
                return
            
            try:
                await category.set_permissions(ctx.guild.default_role, view_channel=False)
                await category.set_permissions(role, view_channel=True)
                await textChannel.set_permissions(ctx.guild.default_role, view_channel=False)
                await textChannel.set_permissions(role, view_channel=True, send_messages=True, manage_messages=True, read_messages=True)
                await voiceChannel.set_permissions(ctx.guild.default_role, view_channel=False, connect=False)
                await voiceChannel.set_permissions(role, view_channel=True, connect=True)

                message += f"Set channel permissions for {roleName}\n"
            except:
                message += "Failed to set channel permissions: Aborting"
                await ctx.send(message)
                return
            
        # Add team to database
        try:
            DB.add_team(ctx.guild.id, roleName, role.id, category.id, textChannel.id, voiceChannel.id)
        except:
            message += "Problem in database: Aborting"
            await ctx.send(message)
            return
        
        await ctx.send(message.rstrip('\n'))


    @commands.command(aliases=['teamRoleReact'])
    @commands.guild_only()
    async def teamRoleReaction(self, ctx, role: discord.Role):

        """Sends a message to assign teams based on reacts
        The bot will send a message and anyone who reacts to it will get assigned/unassigned to the corresponding team
        If a user attempts to join multiple teams, will get unassigned from the previous one
        This command is admin only"""

        if (not ctx.author.guild_permissions.administrator):
            await ctx.send(macros.FORBIDDEN_EMOTE + " Only admins can use this command")
            return
        
        team = DB.get_team_from_role(ctx.guild.id, role.id)
        if team == None:
            await ctx.send(f"{macros.FORBIDDEN_EMOTE} Role {role.name} does not correspond to a team!")
            return

        message = await ctx.send(f"To enter {role.mention} use the {macros.REACT_EMOTE} react below!\nWarning: Joining another team will get you unassigned from the previous one")
        await message.add_reaction(macros.REACT_EMOTE)

        try:
            DB.add_team_role_reaction(ctx.guild.id, message.id, ctx.channel.id, team.team_id)
        except:
            await message.delete()
            return


    # TODO:
    # @commands.command()
    # @commands.guild_only()
    # async def disableRoleReactions(self, ctx):

    #     """Disables all previous role reactions
    #     All role reactions in this channel will be edited to mention they are no longer valid and any reacts on them will be ignored
    #     This command is admin only"""

    #     if (not ctx.author.guild_permissions.administrator):
    #         await ctx.send(macros.FORBIDDEN_EMOTE + " Only admins can use this command")
    #         return

    #     messages = None
    #     try:
    #         messages = DB.get_message_react_pairs(ctx.guild.id)
    #     except:
    #         ctx.send("Couldn't retrive database pairs: Aborting")
    #         return

    #     try:
    #         DB.deleteGuildRoleReactions(ctx.guild.id)
    #     except:
    #         await ctx.send("Failed to commit database transaction: Aborting")
    #         return

    #     for p in messages:
    #         message = await (ctx.guild.get_channel(p[1])).fetch_message(p[0])
    #         await message.edit(content=message.content + "\nThis message has been deactivated, reacts will have no more effect from now on")

    #     await ctx.send("All previous messages are now invalid")



# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(AdminCog(bot))
