# pong.py
import pygame
import sys

class PongGame:
    WIDTH, HEIGHT = 640, 480
    PADDLE_W, PADDLE_H = 10, 80
    BALL_SIZE = 16
    SPEED = 5

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        self.reset()

    def reset(self):
        # paddles: [x, y]
        self.left_paddle = [10, self.HEIGHT//2 - self.PADDLE_H//2]
        self.right_paddle = [self.WIDTH - 10 - self.PADDLE_W, self.HEIGHT//2 - self.PADDLE_H//2]
        # ball: [x, y, dx, dy]
        self.ball = [self.WIDTH//2 - self.BALL_SIZE//2,
                     self.HEIGHT//2 - self.BALL_SIZE//2,
                     self.SPEED, self.SPEED]
        # scores
        self.score_left = 0
        self.score_right = 0

    def draw(self):
        self.screen.fill((0,0,0))
        # draw paddles
        pygame.draw.rect(self.screen, (200,200,200), (*self.left_paddle, self.PADDLE_W, self.PADDLE_H))
        pygame.draw.rect(self.screen, (200,200,200), (*self.right_paddle, self.PADDLE_W, self.PADDLE_H))
        # draw ball
        pygame.draw.ellipse(self.screen, (200,200,200), (*self.ball[:2], self.BALL_SIZE, self.BALL_SIZE))
        # draw net
        for y in range(0, self.HEIGHT, 20):
            pygame.draw.rect(self.screen, (100,100,100), (self.WIDTH//2-1, y, 2, 10))
        # draw scores
        left_txt = self.font.render(str(self.score_left), True, (200,200,200))
        right_txt = self.font.render(str(self.score_right), True, (200,200,200))
        self.screen.blit(left_txt, (self.WIDTH//4, 20))
        self.screen.blit(right_txt, (self.WIDTH*3//4, 20))
        pygame.display.flip()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        # W/S for left paddle
        if keys[pygame.K_w] and self.left_paddle[1] > 0:
            self.left_paddle[1] -= self.SPEED
        if keys[pygame.K_s] and self.left_paddle[1] + self.PADDLE_H < self.HEIGHT:
            self.left_paddle[1] += self.SPEED
        # Up/Down for right paddle
        if keys[pygame.K_UP] and self.right_paddle[1] > 0:
            self.right_paddle[1] -= self.SPEED
        if keys[pygame.K_DOWN] and self.right_paddle[1] + self.PADDLE_H < self.HEIGHT:
            self.right_paddle[1] += self.SPEED

    def update_ball(self):
        # move ball
        self.ball[0] += self.ball[2]
        self.ball[1] += self.ball[3]
        # top/bottom collision
        if self.ball[1] <= 0 or self.ball[1] + self.BALL_SIZE >= self.HEIGHT:
            self.ball[3] *= -1
        # paddle collision
        ball_rect = pygame.Rect(*self.ball[:2], self.BALL_SIZE, self.BALL_SIZE)
        lp_rect = pygame.Rect(*self.left_paddle, self.PADDLE_W, self.PADDLE_H)
        rp_rect = pygame.Rect(*self.right_paddle, self.PADDLE_W, self.PADDLE_H)
        if ball_rect.colliderect(lp_rect) or ball_rect.colliderect(rp_rect):
            self.ball[2] *= -1
        # score?
        if self.ball[0] <= 0:
            self.score_right += 1
            self.reset_ball(direction=1)
        if self.ball[0] + self.BALL_SIZE >= self.WIDTH:
            self.score_left += 1
            self.reset_ball(direction=-1)

    def reset_ball(self, direction=1):
        # center ball and send toward scorer's side
        self.ball[0] = self.WIDTH//2 - self.BALL_SIZE//2
        self.ball[1] = self.HEIGHT//2 - self.BALL_SIZE//2
        self.ball[2] = self.SPEED * direction
        self.ball[3] = self.SPEED

    def run(self):
        self.reset()
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            self.handle_input()
            self.update_ball()
            self.draw()
            self.clock.tick(60)
