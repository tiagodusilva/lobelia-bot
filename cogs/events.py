from cogs.utils.dbInterface import DbInterface as DB
import cogs.utils.botMacros as macros

import discord
from discord.ext import commands


class EventsCog(commands.Cog, name="Events"):

    def __init__(self, bot):
        self.bot = bot

    async def on_raw_reaction(self, payload):
        # Only listen to reactions on messages made by the bot and whose emote matches 
        if (payload.user_id == macros.BOT_ID or not payload.emoji.name in macros.REACTS):
            return None, None

        team = DB.get_team_from_role_reaction(payload.guild_id, payload.channel_id, payload.message_id)
        if (team == None):
            return None, None, None

        guild = self.bot.get_guild(payload.guild_id)
        return team, guild, guild.get_member(payload.user_id)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_add(self, payload):
        try:
            team, guild, member = await self.on_raw_reaction(payload)
            if team == None:
                return

            new_role = guild.get_role(team.role_id)

            old_team = DB.get_member_team(payload.guild_id, member)
            if old_team != None:
                old_role = guild.get_role(old_team.role_id)
                await member.remove_roles(old_role)
                await member.add_roles(new_role)
                await guild.system_channel.send(f"Member {member.mention} changed from team {old_role.name} to team {new_role.name}")
            else:
                await member.add_roles(new_role)
                await guild.system_channel.send(f"Member {member.mention} joined team {new_role.name}")
        except:
            pass

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_remove(self, payload):
        try:
            team, guild, member = await self.on_raw_reaction(payload)
            if team == None:
                return

            role = guild.get_role(team.role_id)
            await member.remove_roles(role)
            # TODO: Fix message once we remove reacts on the other event
            await guild.system_channel.send(f"Member {member.mention} (may have) left team {role.name}")
        except:
            pass



    @commands.Cog.listener()
    @commands.guild_only()
    async def on_guild_role_delete(self, role):
        team = DB.get_team_from_role(role.guild.id, role.id)
        if team != None:            
            DB.delete_team(team.team_id)
            await role.guild.system_channel.send(f"Warning: Role {role.name} was manually deleted")

    
    # @commands.Cog.listener()
    # @commands.guild_only()
    # async def on_guild_role_update(self, before, after):
    #     if (before.name == after.name or not DB.roleIsTeam(before.guild.id, before.id)):
    #         return
        
    #     DB.updateTeamName(before.guild.id, before.id, after.name)
    #     print(f"Updated database role name of {before.name} to {after.name} from guild {before.guild.name}")


    @commands.Cog.listener()
    @commands.guild_only()
    async def on_member_join(self, member: discord.Member):
        welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
        if welcome_channel != None:
            await welcome_channel.send(f"Welcome to {member.guild.name} {member.mention}")


# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(EventsCog(bot))
