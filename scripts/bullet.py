import pygame, random
from scripts.timer import Timer
import math

class Bullet:
    def __init__(self, game, pos, window, animations, animationsM, bulletType):
        self.window = window
        self.bulletT = bulletType
        self.speed = bulletType[2]
        self.bpos = pos
        self.animation = animations
        self.animationM = animationsM
        self.game = game

    def update(self):
        self.bpos[1] -= self.speed
        self.t = pygame.time.get_ticks()/2
        print(self.bpos[0])
        self.bpos[0] += self.bulletT[1](self.t)
        print(self.bpos[0], self.bulletT[1](self.t))
        # print(self.bpos[0] - (self.game.player.pos[0]+(self.game.assets['ships/blue'].images[0].get_width()/2) - (self.game.assets['rockets/blue'].images[0].get_width()/2)))
        self.animation.update()
        self.animationM.update()
        print(self.bpos[0])
        print("________________________________________________________________")
    def render(self):
        mask = pygame.mask.from_surface(self.animationM.img())
        # outline = [(p[0] + self.bpos[0], p[1] + self.bpos[1]) for p in mask.outline(every=1)]
        # pygame.draw.lines(self.window, (255, 0, 255), False, outline, 3)
        self.window.blit(self.animation.img(), self.bpos)
        return mask

class BulletManager:
    def __init__(self, game, window, color):
        self.game = game
        self.window = window
        self.color = color
        self.bullets = []
        self.animation = self.game.assets[f"rockets/{self.color}"].copy()
        self.animationM = self.game.assets["rocketsM"].copy()
        self.timer = None
        self.bulletsT = {  #for the image tilting make a seperate img folder and animate that if using code doesn't work
            'normal': [0, 0, 2.5, 1],
            # put price, amplitude, speed, cooldown;
            'sin': {'type': 'level',
                    1: [100, lambda x: round(math.sin(x/10) * 5, 0), 5.5, 0.1],
                    2: [100, lambda x: round(math.sin(x/12) * 5, 0), 5.5, 0.05],
                    3: [100, lambda x: round(math.sin(x/17) * 5, 0), 5.5, 0.025],
                    4: [100, lambda x: round(math.sin(x/23) * 5, 0), 5.5, 0.0125],
                    5: [100, lambda x: round(math.sin(x/28) * 5, 0), 5.5, 0]},
            'multi': {'type': 'multiple',
                      1: [100, lambda x: -5, 5, 1],
                      2: [100, lambda x: 0, 2.5, 1],
                      3: [100, lambda x: 5, 5, 1]}
        }
        self.currentBullet = self.bulletsT['sin']
        self.blevel = 1
    
    def setColor(self, color):
        self.color = color
        self.animation = self.game.assets[f"rockets/{self.color}"].copy()

    
    def shoot(self, pos):
        if self.timer == None:
            self.timer = Timer(self.currentBullet[self.blevel][3])
            if self.currentBullet['type'] == 'level':
                self.bullets.append(Bullet(self.game, pos, self.window, self.animation, self.animationM, self.currentBullet[self.blevel]))
            else:
                # for index, bul in enumerate(self.currentBullet):
                    # if index != 0: self.bullets.append(Bullet(self.game, pos, self.window, self.animation, self.animationM, self.currentBullet[index])); print(index)
                self.bullets.append(Bullet(self.game, pos, self.window, self.animation, self.animationM, self.currentBullet[1]))
                self.bullets.append(Bullet(self.game, pos, self.window, self.animation, self.animationM, self.currentBullet[2]))
                self.bullets.append(Bullet(self.game, pos, self.window, self.animation, self.animationM, self.currentBullet[3]))
                # print(self.bullets)
    
    def update(self):
        for bullet in self.bullets:
            bullet.update()
            # print(bullet.bpos)
            if bullet.bpos[1] <= -5:
                self.bullets.remove(bullet)
        if self.timer != None:
            if self.timer.count(): self.timer = None
    
    def render(self, asteroids = None):
        # print(self.bullets)
        for bullet in self.bullets:
            mask = bullet.render()
            for mas in asteroids:
                overlap = mas.mask.overlap(mask, (bullet.bpos[0]-mas.pos[0], bullet.bpos[1]-mas.pos[1]))
                if overlap != None: 
                    self.game.poss.remove([mas.pos[0], mas.pos[1], self.game.assets["asteroids"][mas.size].get_width(), self.game.assets["asteroids"][mas.size].get_height()])
                    self.bullets.remove(bullet)
                    asteroids.remove(mas)
                    break

        return asteroids
