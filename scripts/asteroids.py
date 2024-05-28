class Asteroid:
    def __init__(self, game, window, size, pos, shadow = True):
        self.size = size
        self.speed = 1
        self.shadow = shadow
        self.window = window
        self.game = game
        self.pos = pos
    
    def update(self):
        self.pos[1] += self.speed

    def render(self):
        self.window.blit(self.game.assets["asteroids"][self.size-1], self.pos)
