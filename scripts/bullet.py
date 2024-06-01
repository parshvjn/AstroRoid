import pygame, random
from scripts.timer import Timer

class Bullet:
    def __init__(self, pos, window, speed, animations, animationsM):
        self.window = window
        self.speed = speed
        self.bpos = pos
        self.animation = animations
        self.animationM = animationsM

    def update(self):
        self.bpos[1] -= self.speed
        self.animation.update()
        self.animationM.update()
    
    def render(self):
        mask = pygame.mask.from_surface(self.animationM.img())
        outline = [(p[0] + self.bpos[0], p[1] + self.bpos[1]) for p in mask.outline(every=1)]
        pygame.draw.lines(self.window, (255, 0, 255), False, outline, 3)
        self.window.blit(self.animation.img(), self.bpos)
        return [mask, self.bpos[0], self.bpos[1]]

class BulletManager:
    def __init__(self, game, window, color):
        self.game = game
        self.window = window
        self.color = color
        self.bullets = []
        self.animation = self.game.assets[f"rockets/{self.color}"].copy()
        self.animationM = self.game.assets["rocketsM"].copy()
        self.speed = 1.5
        self.cooldown = 0
        self.timer = None
    
    def setColor(self, color):
        self.color = color
        self.animation = self.game.assets[f"rockets/{self.color}"].copy()

    
    def shoot(self, pos):
        if self.timer == None:self.timer = Timer(self.cooldown); self.bullets.append(Bullet(pos, self.window, self.speed, self.animation, self.animationM))
    
    def update(self):
        for bullet in self.bullets:
            bullet.update()
            # print(bullet.bpos)
            if bullet.bpos[1] <= -5:
                self.bullets.remove(bullet)
        if self.timer != None:
            if self.timer.count(): self.timer = None
    
    def render(self, asteroids = None):
        for bullet in self.bullets:
            mask = bullet.render()
            for mas in asteroids:
                print(mas[3])
                overlap = mas[0].overlap(mask[0], (bullet.bpos[0]-mas[1], bullet.bpos[1]-mas[2]))
                if overlap != None: self.bullets.remove(bullet);mas[4] = True
        return asteroids
