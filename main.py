import pygame, sys, random
from scripts.player import Player
from scripts.asteroids import Asteroid
from scripts.utils import *
from scripts.bullet import BulletManager
from scripts.button import Button

class Game:
    def __init__(self):
        pygame.init()
        self.winW, self.winH = 1280, 960
        self.surfW, self.surfH = 320, 240
        self.window = pygame.display.set_mode((self.winW, self.winH))
        pygame.display.set_caption("AstroRoid")
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((self.surfW, self.surfH))
        self.assets = {
            'asteroids': load_images("asteroids", scaleFactor=1),
            'asteroidsM': load_images("asteroids", scaleFactor=1, mask = True),
            'rockets/blue': Animation(load_images("rocket/blue"), img_dur=7),
            'rocketsM': Animation(load_images("rocket/blue", mask = True), img_dur=7),
            'rockets/dark': Animation(load_images("rocket/dark"), img_dur=7),
            'rockets/red': Animation(load_images("rocket/red"), img_dur=7),
            'shadows/asteroid': load_images("shadows/asteroids", alpha= 80),
            'shadows/spaceship': Animation(load_images("shadows/spaceship")),
            'ships/blue': Animation(load_images("ship/blue")),  
            'ships/red': Animation(load_images("ship/red")),
            'shipsM': Animation(load_images("shipMask", mask= True)),
            'space': [Animation(load_images(f"space/{x}", scaleFactor=0.5), img_dur=15) for x in range(1, 10)],
            'title': load_image("title.png", scaleFactor= 0.5)
        }

        self.player = Player(self.display, [(self.surfW/2)-(self.assets['ships/blue'].images[0].get_width()/2), self.surfH-self.assets["ships/blue"].images[0].get_height()-2], "blue", self, True)
        self.movement = [False, False]
        self.movement1 = [False, False]
        self.asteroids = []
        self.poss = []
        self.Bullet = BulletManager(self, self.display, "blue")
        self.font = pygame.font.SysFont("assets/fonts/Poppins-SemiBold.ttf", 20)
                                                     
        #buttons
        self.playb = Button("Ignite?", 60, 20, ((self.surfW/2)-30, self.surfH + 25), 4, self.font, self.display, self)
        self.score = 0
        self.highscore = 0
        data = open('saved.txt')
        try:
            self.highscore = int(data.read().split(':')[-1])
        except:
            pass
        data.close()

    def draw_text(self, text, font, text_col, x, y, surf):
        img = font.render(text, True, text_col)
        surf.blit(img, (x, y))
    
    def menu(self):
        self.i2 = 0
        self.i3 = 0
        self.bgAnim = self.assets["space"][random.randint(0,8)].copy()
        self.playbPressed = False
        titley = -40
        while True:
            self.bgAnim.update()
            self.display.blit(self.bgAnim.img(), (0,0))
            self.display.blit(self.bgAnim.img(), (160,0))
            self.display.blit(self.bgAnim.img(), (0,160))
            self.display.blit(self.bgAnim.img(), (160,160))
            titley = min(titley + 2, 75)
            self.display.blit(self.assets["title"],(68, titley))
            # print(titley)
            #menu animation:
            if self.i2 >= 10 and self.i2 <= 55:
                self.playb.draw("game", 2.5, 0)
            elif self.i2 >= 56 and self.i2 <= 107:
                self.playb.draw("game", 0, (self.i2 - 56)*5)
            else:
                if not self.playbPressed:
                    self.playb.draw("game")
                    if self.playb.pressed: self.playbPressed = True
                else:
                    if self.i3 >= 0 and self.i3 <= 10:
                        self.playb.draw("game", 0, 255, -3)
                        self.player.temppos[1] -= 4
                    elif self.i3 >= 11 and self.i3 <= 90:
                        self.playb.draw("game", 0, 255,6)
                        self.player.temppos[1] -= 4
                    else:
                        self.playb.draw("game", 0, 255,0, True)
                        self.player.temppos = [(self.surfW/2)-(self.assets['ships/blue'].images[0].get_width()/2), self.surfH-self.assets["ships/blue"].images[0].get_height()-2]
                        self.i3 = 0
                        self.playb.top_rect = pygame.Rect(130, 261, 60, 20)
                        self.playbPressed = False
                        self.playb.pressed = False
                    self.i3 += 1

            self.player.update()
            self.player.render(True)
            # print(self.player.temppos)
            #######
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            if self.i2 < 108: self.i2 += 1
            self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), (0,0))
            self.clock.tick(60)
            pygame.display.update()
                    

    def main(self):
        self.running = True
        self.i = 0
        while self.running:
            self.display.fill((255, 56, 48))
            # self.display.fill((0,0,0))
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
                    if event.key == pygame.K_SPACE:
                        self.Bullet.shoot([self.player.pos[0]+(self.assets['ships/blue'].images[0].get_width()/2) - (self.assets['rockets/blue'].images[0].get_width()/2), self.player.pos[1]])
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.movement = [False, False]
                        self.movement1 = [False, False]
                        self.bgAnim = self.assets["space"][random.randint(0,8)].copy()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement1[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement1[1] = False
            self.Bullet.update()
            self.Bullet.render(self.asteroids)
            self.player.update(self.movement, self.movement1)
            self.player.pos[0] %= self.surfW
            self.player.render()
            for asteroid in self.asteroids:
                # if self.i <180: # i use this to pause the asteroids' movement, so i can test something
                #     asteroid.update()
                asteroid.update()
                asteroid.render()
                if asteroid.pos[1] -2 >= self.surfH:
                    self.asteroids.remove(asteroid)
                    self.poss.remove([asteroid.pos[0], asteroid.pos[1], self.assets["asteroids"][asteroid.size].get_width(), self.assets["asteroids"][asteroid.size].get_height()])
            
            if self.i % 15 == 0:
                for x in range(3):
                    ast = random.randint(0, 5)
                    astWidth, astHeight = self.assets["asteroids"][ast].get_width(), self.assets["asteroids"][ast].get_height()
                    pos = [random.randint(0, self.surfW - 1 - astWidth), -astHeight - 1, astWidth, astHeight]
                    self.asteroids.append(Asteroid(self, self.display, ast, pos)); self.poss.append(pos)
            
            self.i += 1

            self.draw_text("FPS: " + str(round(self.clock.get_fps(), 2)), self.font, pygame.Color("azure"), 10, 10, self.display)
            self.draw_text("Score: " + str(self.score), self.font, pygame.Color("azure"), 10, 22, self.display)
            self.draw_text("High: " + str(self.highscore), self.font, pygame.Color("azure"), 10, 34, self.display)
            self.score += 1

            self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    Game().menu()
