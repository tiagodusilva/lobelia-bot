class Team:
    """
    Class to model the data preserved for each team
    """

    def __init__(self, team_id, guild_id, role_id, name, category_channel_id, text_channel_id, voice_channel_id):
        super().__init__()
        self.team_id = team_id
        self.guild_id = guild_id
        self.role_id = role_id
        self.name = name
        self.text_channel_id = text_channel_id
        self.voice_channel_id = voice_channel_id
        self.category_channel_id = category_channel_id

    @staticmethod
    def from_db(obj):
        pass
    
    def __eq__(self, value):
        return super().__eq__(value)
