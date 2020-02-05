# GUI 표현해주는 내용
import pygame
import time
pygame.init()

window = pygame.display.set_mode((1000, 656))
window.fill((255, 255, 255))
pygame.display.update()

is_end = False

def drow_ice_image():
    window.blit(pygame.image.load("car_ice_icon.png"), (0, 0))
    pygame.display.update()


def drow_image():
    window.blit(pygame.image.load("car_no_icon.png"), (0, 0))
    pygame.display.update()


while True:
    print("A")
    drow_image()
    time.sleep(1)

    print("B")
    drow_ice_image()
    time.sleep(1)
    pygame.display.update()

pygame.quit()
quit()
