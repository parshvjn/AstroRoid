import pygame, sys, random
from scripts.player import Player
from scripts.asteroids import Asteroid
from scripts.utils import *

class Game:
    def __init__(self):
        self.winW, self.winH = 1280, 960
        self.surfW, self.surfH = 320, 240
        self.window = pygame.display.set_mode((self.winW, self.winH))
        pygame.display.set_caption("AstroRoid")
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((self.surfW, self.surfH))
        self.assets = {
            'asteroids': load_images("asteroids", scaleFactor=1.2),
            'rockets/blue': load_images("rocket/blue"),
            'rockets/dark': load_images("rocket/dark"),
            'rockets/red': load_images("rocket/red"),
            'shadows/asteroid': load_images("shadows/asteroids"),
            'shadows/spaceship': load_images("shadows/spaceship"),
            'ships/blue': load_images("ship/blue"),
            'ships/red': load_images("ship/red")
        }

        self.player = Player(self.display, [10, 20], "blue", self, True)
        self.movement = [False, False]
        self.movement1 = [False, False]
        self.asteroids = []
        self.astIter = 0
        self.poss = []


    def main(self):
        self.running = True
        self.i = 0
        while self.running:
            self.display.fill((255, 56, 48))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement1[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement1[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement1[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement1[1] = False
            self.player.update(self.movement, self.movement1)
            self.player.render()
            for asteroid in self.asteroids:
                asteroid.update()
                asteroid.render()
                if asteroid.pos[1] -2 >= self.surfH:
                    self.asteroids.remove(asteroid)
                    self.poss.remove([asteroid.pos[0], asteroid.pos[1], self.assets["asteroids"][asteroid.size].get_width(), self.assets["asteroids"][asteroid.size].get_height()])
            
            if self.i % 15 == 0:
                rects = []
                self.astIter += 1
                for x in range(3):
                    cancel = False
                    ast = random.randint(0, 5)
                    astWidth, astHeight = self.assets["asteroids"][ast].get_width(), self.assets["asteroids"][ast].get_height()
                    pos = [random.randint(0, self.surfW - 1 - astWidth), -astHeight - 1, astWidth, astHeight]
                    # for pos1 in self.poss:
                    #     if pos[0] + self.assets["asteroids"][ast].get_width()> pos1[0] and pos[0] < pos1[0] + self.assets["asteroids"][ast].get_width():
                    #         if pos[1] + self.assets["asteroids"][ast].get_height() > pos1[1] and pos[1] < pos1[1] + self.assets["asteroids"][ast].get_height():
                    #             cancel = True
                    tempRect = pygame.Rect(pos[0], pos[1], astWidth, astHeight)
                    for rect in rects:
                        if rect.colliderect(tempRect):
                            print('cancel')
                            cancel = True
                    for index, asteroid in enumerate(self.asteroids):
                        self.poss[index][1] = asteroid.pos[1]
                    for pos1 in self.poss:
                        rects.append(pygame.Rect(pos1[0], pos1[1], pos1[2], pos1[3]))

                    if not cancel: self.asteroids.append(Asteroid(self, self.display, ast, pos)); self.poss.append(pos)
                # print(rects)
            
            self.i += 1

            self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()

if __name__ == '__main__':
    Game().main()
