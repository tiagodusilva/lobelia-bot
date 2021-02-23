drop table if exists Team;
CREATE TABLE Roles(
    id INT NOT NULL PRIMARY KEY,
    guild_id INT NOT NULL,
    role_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    text_channel_id INT NOT NULL,
    category_channel_id INT NOT NULL,
    voice_channel_id INT NOT NULL,
    UNIQUE(guild_id, role_id)
);

drop table if exists TeamRoleReaction;
CREATE TABLE RoleReaction(
    guild_id INT NOT NULL,
    message_id INT NOT NULL,
    channel_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY(guild_id, message_id, channel_id, role_id)
);
