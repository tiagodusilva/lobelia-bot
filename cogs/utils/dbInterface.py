import cogs.utils.botMacros as macros

import sqlite3

import discord
from discord.ext import commands

from models.team import Team

from contextlib import closing

_connection = sqlite3.connect(macros.DB_FILE)

class DbInterface():

    # ROLE REACTIONS

    @staticmethod
    def add_team_role_reaction(guild_id, message_id, channel_id, team_id):
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            cursor.execute(
                "INSERT INTO TeamRoleReaction (guild_id, channel_id, message_id, team_id) VALUES (?, ?, ?, ?)",
                (guild_id, channel_id, message_id, team_id)
            )
            _connection.commit()

    @staticmethod
    def get_team_role_reaction_role(guild_id, channel_id, message_id):
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            role_id = cursor.execute(
                """SELECT FROM TeamRoleReaction role_id
                    WHERE guild_id = ? AND channel_id = ? AND message_id = ?
                    INNER JOIN Team ON(TeamRoleReaction.team_id = Team.id)
                """,
                (guild_id, channel_id, message_id)
            ).fetchone()
            return role_id[0] if role_id != None else None

    @staticmethod
    def get_team_role_reaction_channel_messages(guild_id, channel_id):
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            return cursor.execute(
                """SELECT message_id
                    FROM TeamRoleReaction
                    WHERE guild_id = ? AND channel_id = ?
                """,
                (guild_id, channel_id)
            ).fetchall()

    @staticmethod
    def delete_role_reaction_from_channel(guild_id, channel_id):
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            cursor.execute("DELETE FROM TeamRoleReaction WHERE guild_id=? AND channel_id=?", (guild_id, channel_id))
            _connection.commit()


    # TEAMS
    @staticmethod
    def add_team(guild_id, team_name, role_id, category_channel_id, text_channel_id, voice_channel_id):
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            cursor.execute(
                "INSERT INTO Team (guild_id, role_id, name, category_channel_id, text_channel_id, voice_channel_id) VALUES (?, ?, ?, ?, ?, ?)",
                (guild_id, role_id, team_name, category_channel_id, text_channel_id, voice_channel_id)
            )
            _connection.commit()

    @staticmethod
    def delete_team(team_id):
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            cursor.execute(
                """DELETE FROM Team
                    WHERE id = ?
                """,
                (team_id, )
            )
            _connection.commit()

    @staticmethod
    def get_team_from_role_reaction(guild_id, channel_id, message_id):
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            team = cursor.execute(
                """SELECT id, Team.guild_id, role_id, name, category_channel_id, text_channel_id, voice_channel_id
                    FROM TeamRoleReaction
                    INNER JOIN Team ON(TeamRoleReaction.team_id = Team.id)
                    WHERE TeamRoleReaction.guild_id = ? AND channel_id = ? AND message_id = ?
                """,
                (guild_id, channel_id, message_id)
            ).fetchone()
            return Team(*team) if team != None else None

    @staticmethod
    def get_team_from_role(guild_id, role_id):
        if (role_id == None): return None

        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            team = cursor.execute(
                """SELECT id, guild_id, role_id, name, category_channel_id, text_channel_id, voice_channel_id
                    FROM Team
                    WHERE guild_id = ? AND role_id = ?
                """,
                (guild_id, role_id)
            ).fetchone()
            return Team(*team) if team != None else None
    
    @staticmethod
    def get_team_from_text_channel(guild_id, channel_id):
        if (channel_id == None): return None

        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            team = cursor.execute(
                """SELECT id, guild_id, role_id, name, category_channel_id, text_channel_id, voice_channel_id
                    FROM Team
                    WHERE guild_id = ? AND text_channel_id = ?
                """,
                (guild_id, channel_id)
            ).fetchone()
            return Team(*team) if team != None else None


    @staticmethod
    def get_team_from_id(guild_id, team_id):
        if (team_id == None): return None

        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            team = cursor.execute(
                """SELECT FROM id, guild_id, role_id, name, category_channel_id, text_channel_id, voice_channel_id
                    FROM Team
                    WHERE guild_id = ? AND id = ?
                """,
                (guild_id, team_id)
            ).fetchone()
            return Team(*team) if team != None else None


    @staticmethod
    def get_team_from_name(guild_id, name):
        if (name == None): return None

        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            team = cursor.execute(
                """SELECT id, guild_id, role_id, name, category_channel_id, text_channel_id, voice_channel_id
                    FROM Team
                    WHERE guild_id = ? AND name like ?
                """,
                (guild_id, name)
            ).fetchone()
            return Team(*team) if team != None else None
    


    @classmethod
    def get_member_team(cls, guild_id, member):
        """
        Returns the team the member belongs to
        Otherwise returns None
        """
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            cursor.execute(
                """SELECT role_id
                    FROM Team
                    WHERE guild_id = ?
                """,
                (guild_id, )
            )
            while True:
                team_role = cursor.fetchone()
                if team_role == None:
                    return None
                role = discord.utils.get(member.roles, id=team_role)
                if role != None:
                    return cls.get_team_from_role(guild_id, role.id)





# ---------------------------------------


    # @staticmethod
    # def get_message_react_pairs(guild_id):
    #     with closing(_connection.cursor()) as cursor:
    #         cursor = _connection.cursor()
    #         return cursor.execute("SELECT message_id, channel_id, role_id FROM RoleReaction WHERE guild_id=?", (guild_id, )).fetchall()

    # @staticmethod
    # def getTeams(guild_id):
    #     with closing(_connection.cursor()) as cursor:
    #         cursor = _connection.cursor()
    #         return cursor.execute("SELECT role_id, role_name FROM Roles WHERE guild_id=?", (guild_id, )).fetchall()

    # @staticmethod
    # def replaceRole(guild_id, role_id, role_name):
    #     with closing(_connection.cursor()) as cursor:
    #         cursor = _connection.cursor()
    #         cursor.execute("REPLACE INTO Roles VALUES (?, ?, ?)", (guild_id, role_id, role_name))
    #         _connection.commit()
    
    # @staticmethod
    # def updateTeamName(guild_id, role_id, role_name):
    #     with closing(_connection.cursor()) as cursor:
    #         cursor = _connection.cursor()
    #         cursor.execute("UPDATE Roles SET role_name=? WHERE guild_id=? AND role_id=?", (guild_id, role_id, role_name))
    #         _connection.commit()

    # @staticmethod
    # def addRoleReaction(guild_id, message_id, channel_id, role_id):
    #     with closing(_connection.cursor()) as cursor:
    #         cursor = _connection.cursor()
    #         message_ids = cursor.execute("INSERT INTO RoleReaction VALUES(?, ?, ?, ?)", (guild_id, message_id, channel_id, role_id)).fetchall()
    #         _connection.commit()

    # @staticmethod
    # def deleteGuildRoleReactions(guild_id):
    #     with closing(_connection.cursor()) as cursor:
    #         cursor = _connection.cursor()
    #         cursor.execute("DELETE FROM RoleReaction WHERE guild_id=?", (guild_id, ))
    #         _connection.commit()

    # @staticmethod
    # def deleteRoleReaction(guild_id, role_id):
    #     with closing(_connection.cursor()) as cursor:
    #         cursor = _connection.cursor()
    #         cursor.execute("DELETE FROM RoleReaction WHERE guild_id=? AND role_id=?", (guild_id, role_id))
    #         _connection.commit()
    #     pass

    # @staticmethod
    # def deleteTeamRole(guild_id, role_id):
    #     with closing(_connection.cursor()) as cursor:
    #         cursor = _connection.cursor()
    #         cursor.execute("DELETE FROM Roles WHERE guild_id=? AND role_id=?", (guild_id, role_id))
    #         _connection.commit()

    # @classmethod
    # def roleIsTeam(cls, guild_id, role_id):
    #     return role_id in (v[0] for v in cls.getTeams(guild_id))

    # @classmethod
    # def hasTeam(cls, guild_id, teamName):
    #     for team in cls.getTeams(guild_id):
    #         if (team[1] == teamName):
    #             return True
        
    #     return False

    # @classmethod
    # def getMemberTeamRole(cls, guild_id, roles):
    #     """Assumes that each member can only have one team"""

    #     for team in cls.getTeams(guild_id):
    #         for role in roles:
    #             if (role.id == team[0]):
    #                 return role
        
    #     return None



