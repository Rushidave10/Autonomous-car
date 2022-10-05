import pygame
import time
import math
from utils import scale_image, blit_rotate_center

GRASS = pygame.image.load("graay.jpg")
TRACK = scale_image(pygame.image.load("Safe RL-3 1.jpg"), 0.5)

FINISH_LINE = scale_image(pygame.image.load("finish_line.jpg"), 0.23)

RED_CAR = scale_image(pygame.image.load("red_car.png"), 0.2)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((740, 900))
pygame.display.set_caption("Racing Car")

FPS = 60


class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img= self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.X, self.Y = self.START_POS
        self.acceleration = 0.2

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.X, self.Y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.Y -= vertical
        self.X -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (610, 220)


def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)
    player_car.draw(win)
    pygame.display.update()


run = True
clock = pygame.time.Clock()
images = [(TRACK, (0, 0)), (FINISH_LINE, (610, 200))]
player_car = PlayerCar(10, 4)


while run:
    clock.tick(FPS)  # Fixing the speed of loop to 60 Frame per second
    # WIN.blit(GRASS, (0, 0))  # Not needed

    draw(WIN, images, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Safe closing of window
            run = False
            break

    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player_car.move_forward()
    if not moved:
        player_car.reduce_speed()

pygame.quit()
