# tetris.py
import pygame
import sys
import random

# define tetromino shapes
SHAPES = {
    'I': [[1,1,1,1]],
    'O': [[1,1],
          [1,1]],
    'T': [[0,1,0],
          [1,1,1]],
    'S': [[0,1,1],
          [1,1,0]],
    'Z': [[1,1,0],
          [0,1,1]],
    'J': [[1,0,0],
          [1,1,1]],
    'L': [[0,0,1],
          [1,1,1]]
}
COLORS = {
    'I': (0,240,240),
    'O': (240,240,0),
    'T': (160,0,240),
    'S': (0,240,0),
    'Z': (240,0,0),
    'J': (0,0,240),
    'L': (240,160,0)
}

class TetrisGame:
    ROWS, COLS = 20, 10
    BLOCK = 24

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.grid = [[(0,0,0) for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.score = 0
        self.spawn_piece()
        self.drop_timer = 0

    def spawn_piece(self):
        self.shape_key = random.choice(list(SHAPES.keys()))
        self.shape = [row[:] for row in SHAPES[self.shape_key]]
        self.color = COLORS[self.shape_key]
        self.pos = [0, self.COLS // 2 - len(self.shape[0])//2]

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def valid(self, offset=(0,0)):
        off_x, off_y = offset
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = self.pos[1] + x + off_x
                    ny = self.pos[0] + y + off_y
                    if nx < 0 or nx >= self.COLS or ny >= self.ROWS:
                        return False
                    if ny >= 0 and self.grid[ny][nx] != (0,0,0):
                        return False
        return True

    def lock_piece(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.pos[0]+y][self.pos[1]+x] = self.color
        self.clear_lines()
        self.spawn_piece()
        if not self.valid():
            # game over
            print(f"Game Over! Score: {self.score}")
            return False
        return True

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == (0,0,0) for cell in row)]
        lines_cleared = self.ROWS - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [(0,0,0) for _ in range(self.COLS)])
        self.grid = new_grid
        self.score += lines_cleared ** 2 * 100

    def draw_grid(self):
        for y in range(self.ROWS):
            for x in range(self.COLS):
                pygame.draw.rect(
                    self.screen,
                    self.grid[y][x],
                    (x*self.BLOCK, y*self.BLOCK, self.BLOCK, self.BLOCK),
                    0
                )
                pygame.draw.rect(
                    self.screen,
                    (40,40,40),
                    (x*self.BLOCK, y*self.BLOCK, self.BLOCK, self.BLOCK),
                    1
                )

    def draw_piece(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    px = (self.pos[1]+x)*self.BLOCK
                    py = (self.pos[0]+y)*self.BLOCK
                    pygame.draw.rect(self.screen, self.color, (px, py, self.BLOCK, self.BLOCK))
                    pygame.draw.rect(self.screen, (80,80,80), (px, py, self.BLOCK, self.BLOCK), 1)

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    if self.valid(offset=(0,-1)): self.pos[1] -= 1
                if e.key == pygame.K_RIGHT:
                    if self.valid(offset=(0,1)): self.pos[1] += 1
                if e.key == pygame.K_DOWN:
                    if self.valid(offset=(1,0)): self.pos[0] += 1
                if e.key == pygame.K_UP:
                    self.rotate()
                    if not self.valid(): 
                        # undo rotation
                        for _ in range(3): self.rotate()

    def run(self):
        self.reset()
        while True:
            dt = self.clock.tick(60)
            self.handle_events()
            self.drop_timer += dt
            if self.drop_timer > 500:  # drop every 0.5s
                self.drop_timer = 0
                if not self.valid(offset=(1,0)) or not self.lock_piece():
                    return  # back to menu
                else:
                    self.pos[0] += 1

            self.screen.fill((0,0,0))
            self.draw_grid()
            self.draw_piece()
            pygame.display.flip()
