import pygame

class SMenu:
    def __init__(self, game, window):
        self.window = window
        self.sW, self.sH = 105, 125
        self.surf = pygame.Surface((self.sW, self.sH), pygame.SRCALPHA)
        self.open = 0
        self.stage = None
        self.game = game
    
    def change_state(self, state):
        self.stage = state
    
    def update(self):
        if self.game.firstTime and self.open == 0: self.stage = "open"; self.game.menuB.text = ">"
        if self.stage == "open":
            self.open += 2
            if self.open >= self.sW - 5:
                self.stage = None
        elif self.stage == "close":
            self.open -= 2
            if self.open <= 0:
                self.stage = None
        pygame.draw.rect(self.surf, (0,0,0, 125), pygame.Rect(0, 0, self.sW, self.sH), border_radius= 5)
        self.game.draw_text(f"Coins: {self.game.coins}", self.game.font, (255,255,255), 5, 5, self.surf)
        # pygame.display.update()
    
    def render(self):
        self.window.blit(self.surf, (self.game.surfW - self.open - 7.5, 100))