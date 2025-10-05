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
    
    def resetGame(self):
        self.game.player.pos = [(self.game.surfW/2)-(self.game.assets['ships/blue'].images[0].get_width()/2), self.game.surfH-self.game.assets["ships/blue"].images[0].get_height()-2]
        self.game.asteroids.clear()
        self.game.poss.clear()
        self.game.Bullet.bullets.clear()
        self.game.Bullet.timer = None
        self.game.i = 0
        self.game.coins += int(str(self.game.score)[:-1])
        print(self.game.score, self.game.coins)
        if self.game.score > self.game.highscore: self.game.highscore = self.game.score
        data = open('saved.txt', 'w')
        data.write("highscore:" + str(self.game.highscore))
        data.close()
        self.game.score = 0
        self.game.gameOn = False
        self.game.killCounter +=1
        self.game.firing = False
        self.game.Bullet.n = 0

    def render(self, mask = False):
        self.mask = pygame.mask.from_surface(self.game.assets["asteroidsM"][self.size-1])
        overlap = self.mask.overlap(self.game.player.mask, (self.game.player.pos[0]-self.pos[0], self.game.player.pos[1]-self.pos[1]))
        # outline = [(p[0] + self.pos[0], p[1] + self.pos[1]) for p in self.mask.outline(every=1)]
        # pygame.draw.lines(self.window, (255, 0, 255), False, outline, 3)
        if overlap != None: self.resetGame()
        self.window.blit(self.game.assets['shadows/asteroid'][self.size-1], (self.pos[0]-4, self.pos[1]+3))
        self.window.blit(self.game.assets["asteroids"][self.size-1], self.pos)
