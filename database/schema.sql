PRAGMA foreign_keys = ON;

drop table if exists Team;
CREATE TABLE Team(
    id INTEGER NOT NULL PRIMARY KEY,
    guild_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    text_channel_id INTEGER NOT NULL,
    category_channel_id INTEGER NOT NULL,
    voice_channel_id INTEGER NOT NULL,
    UNIQUE(guild_id, role_id),
    UNIQUE(guild_id, name)
);

drop table if exists TeamRoleReaction;
CREATE TABLE TeamRoleReaction(
    guild_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    PRIMARY KEY(guild_id, channel_id, message_id, team_id)
);
