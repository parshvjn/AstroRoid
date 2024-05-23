import pygame, sys

class Game:
    def __init__(self):
        self.winW, self.winH = 1280, 960
        self.window = pygame.display.set_mode((self.winW, self.winH))
        pygame.display.set_caption("AstroRoid")


    def main(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
        
            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    Game().main()
