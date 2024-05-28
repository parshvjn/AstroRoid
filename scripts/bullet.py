from scripts.timer import Timer
class Bullet:
    def __init__(self, pos, window, speed, animations):
        self.window = window
        self.speed = speed
        self.bpos = pos
        self.animation = animations

    def update(self):
        self.bpos[1] -= self.speed
        self.animation.update()
    
    def render(self):
        self.window.blit(self.animation.img(), self.bpos)

class BulletManager:
    def __init__(self, game, window, color):
        self.game = game
        self.window = window
        self.color = color
        self.bullets = []
        self.animation = self.game.assets[f"rockets/{self.color}"].copy()
        self.speed = 1.5
        self.cooldown = 0.5
        self.timer = None
    
    def setColor(self, color):
        self.color = color
        self.animation = self.game.assets[f"rockets/{self.color}"].copy()

    
    def shoot(self, pos):
        if self.timer == None:self.timer = Timer(self.cooldown); self.bullets.append(Bullet(pos, self.window, self.speed, self.animation))
    
    def update(self):
        for bullet in self.bullets:
            bullet.update()
            print(bullet.bpos)
            if bullet.bpos[1] <= -5:
                self.bullets.remove(bullet)
        if self.timer != None:
            if self.timer.count(): self.timer = None
    
    def render(self):
        for bullet in self.bullets:
            bullet.render()
