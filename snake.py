# snake.py
import pygame
import random
import sys

class SnakeGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.block = 20
        self.reset()

    def reset(self):
        w, h = self.screen.get_size()
        self.snake = [(w//2, h//2)]
        self.dir = (self.block, 0)
        self.spawn_food()
        self.score = 0

    def spawn_food(self):
        w, h = self.screen.get_size()
        self.food = (
            random.randrange(0, w, self.block),
            random.randrange(0, h, self.block)
        )

    def draw(self):
        self.screen.fill((0,0,0))
        # draw snake
        for seg in self.snake:
            pygame.draw.rect(self.screen, (0,255,0), (*seg, self.block, self.block))
        # draw food
        pygame.draw.rect(self.screen, (255,0,0), (*self.food, self.block, self.block))
        pygame.display.flip()

    def handle_keys(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and self.dir != (0, self.block):
                    self.dir = (0, -self.block)
                if e.key == pygame.K_DOWN and self.dir != (0, -self.block):
                    self.dir = (0, self.block)
                if e.key == pygame.K_LEFT and self.dir != (self.block, 0):
                    self.dir = (-self.block, 0)
                if e.key == pygame.K_RIGHT and self.dir != (-self.block, 0):
                    self.dir = (self.block, 0)

    def run(self):
        self.reset()
        while True:
            self.handle_keys()
            # move snake
            head = (self.snake[0][0] + self.dir[0],
                    self.snake[0][1] + self.dir[1])
            self.snake.insert(0, head)
            # check food
            if head == self.food:
                self.score += 1
                self.spawn_food()
            else:
                self.snake.pop()

            # check collisions
            w, h = self.screen.get_size()
            if (head[0] < 0 or head[0] >= w or
                head[1] < 0 or head[1] >= h or
                head in self.snake[1:]):
                print(f"Game Over! Score: {self.score}")
                return  # back to menu

            self.draw()
            self.clock.tick(10)
