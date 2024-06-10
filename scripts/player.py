import pygame
class Player:
    def __init__(self, window, pos: list, color, game, shadows = True):
        self.pos = pos
        self.window = window
        self.game = game
        self.color = color
        self.speed = 2
        self.animation = self.game.assets[f'ships/{self.color}'].copy()
        self.animationShadow = self.game.assets['shadows/spaceship'].copy()
        self.animationMask = self.game.assets['shipsM'].copy()
        self.temppos = [(self.game.surfW/2)-(self.game.assets['ships/blue'].images[0].get_width()/2), self.game.surfH-self.game.assets["ships/blue"].images[0].get_height()-2]

        self.mask = pygame.mask.from_surface(self.animationMask.img())
    
    def colorChange(self):
        self.color = "red" if self.color == "blue" else "blue"
        self.animation = self.game.assets[f'ships/{self.color}'].copy()
    
    def update(self, movement = [0,0], movement1 = [0,0]):
        if movement[0]:
            self.pos[0] -= self.speed
        if movement[1]:
            self.pos[0] += self.speed
        if movement1[0] and self.pos[1] >= 5:
            self.pos[1] -= self.speed
        if movement1[1] and self.pos[1] <= self.game.surfH - self.animation.img().get_height() - 5:
            self.pos[1] += self.speed
        
        self.animation.update()
        self.animationShadow.update()
        self.animationMask.update()

    def render(self, menu = False):
        offset = self.pos[0] - self.game.surfW if self.pos[0] > self.game.surfW else 0
        if menu: self.window.blit(self.animation.img(), self.temppos)
        else:
            self.window.blit(self.animationShadow.img(), (self.pos[0] - 4 - offset, self.pos[1]+3))
            self.window.blit(self.animation.img(), (self.pos[0]-offset, self.pos[1]))
        # print((self.pos[0]-offset, self.pos[1]), self.game.surfW)