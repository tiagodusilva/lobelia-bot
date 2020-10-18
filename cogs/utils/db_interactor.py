import cogs.utils.bot_macros as macros

import sqlite3

import discord
from discord.ext import commands

from contextlib import closing

_connection = sqlite3.connect(macros.DB_FILE)

class DbInteractor():

    @staticmethod
    def get_message_react_pairs(guild_id):
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            return cursor.execute("SELECT message_id, channel_id, role_id FROM RoleReaction WHERE guild_id=?", (guild_id, )).fetchall()

    @staticmethod
    def getTeams(guild_id):
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            return cursor.execute("SELECT role_id, role_name FROM Roles WHERE guild_id=?", (guild_id, )).fetchall()

    @staticmethod
    def replaceRole(guild_id, role_id, role_name):
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            cursor.execute("REPLACE INTO Roles VALUES (?, ?, ?)", (guild_id, role_id, role_name))
            _connection.commit()

    @staticmethod
    def addRoleReaction(guild_id, message_id, channel_id, role_id):
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            message_ids = cursor.execute("INSERT INTO RoleReaction VALUES(?, ?, ?, ?)", (guild_id, message_id, channel_id, role_id)).fetchall()
            _connection.commit()

    @staticmethod
    def deleteGuildRoleReactions(guild_id):
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            cursor.execute("DELETE FROM RoleReaction WHERE guild_id=?", (guild_id, ))
            _connection.commit()

    @staticmethod
    def deleteRoleReaction(guild_id, role_id):
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            cursor.execute("DELETE FROM RoleReaction WHERE guild_id=? AND role_id=?", (guild_id, role_id))
            _connection.commit()
        pass

    @staticmethod
    def deleteTeamRole(guild_id, role_id):
        with closing(_connection.cursor()) as cursor:
            cursor = _connection.cursor()
            cursor.execute("DELETE FROM Roles WHERE guild_id=? AND role_id=?", (guild_id, role_id))
            _connection.commit()

    @classmethod
    def roleIsTeam(cls, guild_id, role_id):
        return role_id in (v[0] for v in cls.getTeams(guild_id))

    @classmethod
    def hasTeam(cls, guild_id, teamName):
        for team in cls.getTeams(guild_id):
            if (team[1] == teamName):
                return True
        
        return False

    @classmethod
    def getMemberTeamRole(cls, guild_id, roles):
        """Assumes that each member can only have one team"""

        for team in cls.getTeams(guild_id):
            for role in roles:
                if (role.id == team[0]):
                    return role
        
        return None



