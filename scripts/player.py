import pygame
class Player:
    def __init__(self, window, pos, color, game, shadows = True):
        self.pos = pos
        self.window = window
        self.game = game
        self.color = color
        self.speed = 2
    
    def colorChange(self):
        self.color = "red" if self.color == "blue" else "blue"
    
    def update(self, movement = [0,0], movement1 = [0,0]):
        if movement[0] and self.pos[0] >= 5:
            self.pos[0] -= self.speed
        if movement[1] and self.pos[0] <= self.game.surfW - self.game.assets[f"ships/{self.color}"][0].get_width() - 5:
            self.pos[0] += self.speed
        if movement1[0] and self.pos[1] >= 5:
            self.pos[1] -= self.speed
        if movement1[1] and self.pos[1] <= self.game.surfH - self.game.assets[f"ships/{self.color}"][0].get_height() - 5:
            self.pos[1] += self.speed

    def render(self):
        self.window.blit(self.game.assets[f"ships/{self.color}"][0], self.pos)