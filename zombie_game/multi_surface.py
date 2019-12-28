import pygame
size = (50,50)
red = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((500,500))

mySurface = pygame.Surface(size)
mySurface.fill((255,255,255))
green_rect = pygame.Rect(25,25,50,50)
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    pygame.draw.rect(mySurface, red, green_rect)
    screen.blit(mySurface, (100,100))
    pygame.display.update()

pygame.quit()
