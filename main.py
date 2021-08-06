import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("RPG Battle")

#load images
#background image
background_img = pygame.image.load("img/Background/background.png").convert_alpha()

# functions

#draw background
def draw_background():
    screen.blit(background_img, (0,0))

run = True

while run:

    clock.tick(fps)
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()