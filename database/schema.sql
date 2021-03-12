PRAGMA foreign_keys = ON;

drop table if exists Team;
CREATE TABLE Team(
    id INT NOT NULL PRIMARY KEY,
    guild_id INT NOT NULL,
    role_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    text_channel_id INT NOT NULL,
    category_channel_id INT NOT NULL,
    voice_channel_id INT NOT NULL,
    UNIQUE(guild_id, role_id),
    UNIQUE(guild_id, name)
);

drop table if exists TeamRoleReaction;
CREATE TABLE TeamRoleReaction(
    guild_id INT NOT NULL,
    channel_id INT NOT NULL,
    message_id INT NOT NULL,
    team_id INT NOT NULL,
    PRIMARY KEY(guild_id, channel_id, message_id, team_id)
);
