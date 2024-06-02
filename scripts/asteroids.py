import pygame, random
class Asteroid:
    def __init__(self, game, window, size, pos: list, shadow = True):
        self.size = size
        self.speed = 1
        self.shadow = shadow
        self.window = window
        self.game = game
        self.pos = pos
        self.mask = pygame.mask.from_surface(self.game.assets["asteroidsM"][self.size-1])
    
    def update(self):
        self.pos[1] += self.speed

    def render(self, mask = False):
        self.mask = pygame.mask.from_surface(self.game.assets["asteroidsM"][self.size-1])
        overlap = self.mask.overlap(self.game.player.mask, (self.game.player.pos[0]-self.pos[0], self.game.player.pos[1]-self.pos[1]))
        outline = [(p[0] + self.pos[0], p[1] + self.pos[1]) for p in self.mask.outline(every=1)]
        pygame.draw.lines(self.window, (255, 0, 255), False, outline, 3)
        # if overlap != None: print('collision')
        self.window.blit(self.game.assets["asteroids"][self.size-1], self.pos)
