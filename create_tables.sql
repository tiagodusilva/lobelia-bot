drop table if exists Roles;
CREATE TABLE Roles(
    guild_id INT NOT NULL,
    role_id INT NOT NULL,
    role_name TEXT NOT NULL,
    PRIMARY KEY(guild_id, role_id)
);

drop table if exists RoleReaction;
CREATE TABLE RoleReaction(
    guild_id INT NOT NULL,
    message_id INT NOT NULL,
    channel_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY(guild_id, message_id, channel_id, role_id)
);
