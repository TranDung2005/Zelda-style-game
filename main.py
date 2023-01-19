import pygame, sys
from settings import SCR_WIDTH, SCR_HEIGHT, WATER_COLOR
from operate import OPERATION


class GAME:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
        pygame.display.set_caption("Zelda")
        self.clock = pygame.time.Clock()

        self.operate = OPERATION()

        self.operate.start_sound.play(-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if not self.operate.game_over:

                        if not self.operate.game_play:
                            if event.key == pygame.K_p:
                                self.operate.start_sound.stop()
                                self.operate.play_sound.play(-1)
                                self.operate.play()
                                   
                        if self.operate.game_play:
                            if event.key == pygame.K_s:
                                self.operate.paused()

                    if self.operate.game_over:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_r:
                            self.operate = self.operate.reset()
                        

            self.screen.fill((WATER_COLOR))
            self.operate.run()
           
            pygame.display.update()
            self.clock.tick(60)

    
if __name__ == '__main__':
    game = GAME()
    game.run()