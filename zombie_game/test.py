import pygame
from math import pi
pygame.init()

screen = pygame.display.set_mode((500,500))
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)

size = (50, 50)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    rect_border = pygame.Surface(size)  # Create a Surface to draw on.
    pygame.draw.rect(rect_border, RED, rect_border.get_rect(), 10)  # Draw on it.

    rect_filled = pygame.Surface(size)
    pygame.draw.rect(rect_filled, RED, rect_filled.get_rect())
    screen.blit(rect_border, (0,0))
    pygame.display.update()

pygame.quit()
