# main.py
import pygame
import sys
from snake import SnakeGame 
from tetris import TetrisGame
from pong import PongGame
from pong_ai import PongGameAI

# --- Game Manager / Menu Shell ---
class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Mini Games Hub")
        self.clock = pygame.time.Clock()
        # register your games here
        self.games = {
            "Snake": SnakeGame(self.screen),
            "Tetris": TetrisGame(self.screen),
            "Pong": PongGame(self.screen),
            "Pong AI": PongGameAI(self.screen),
        }
        self.font = pygame.font.SysFont(None, 48)
        self.selected = 0
        self.keys = list(self.games.keys())

    def draw_menu(self):
        self.screen.fill((30, 30, 30))
        for idx, name in enumerate(self.keys):
            color = (200,200,50) if idx == self.selected else (200,200,200)
            txt = self.font.render(name, True, color)
            self.screen.blit(txt, (240, 150 + idx*60))
        pygame.display.flip()

    def run(self):
        in_menu = True
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if in_menu and e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.keys)
                    if e.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.keys)
                    if e.key == pygame.K_RETURN:
                        in_menu = False
                        # launch selected game
                        game = self.games[self.keys[self.selected]]
                        game.run()
                        in_menu = True

            if in_menu:
                self.draw_menu()
                self.clock.tick(30)

if __name__ == "__main__":
    GameManager().run()
