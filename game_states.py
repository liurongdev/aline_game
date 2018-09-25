

class GameStates():
    def __init__(self,ai_settings):
        self.ai_settings=ai_settings
        self.game_active=False
        self.restart_stat()
        self.high_score=0


    def restart_stat(self):
        self.ships_left=self.ai_settings.ship_limit
        self.score=0
        self.level=1