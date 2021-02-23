class Team:
    """
    Class to model the data preserved for each team
    """

    def __init__(self, guild_id, role_id, name, text_channel_id, voice_channel_id, category_channel_id):
        super().__init__()
        self.guild_id = guild_id
        self.role_id = role_id
        self.name = name
        self.text_channel_id = text_channel_id
        self.voice_channel_id = voice_channel_id
        self.category_channel_id = category_channel_id
    
    def __eq__(self, value):
        return super().__eq__(value)
