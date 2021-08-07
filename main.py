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

#classes
class Fighter():
    def __init__(self, x, y, name , max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        img = pygame.image.load(f"img/{self.name}/Idle/0.png")
        self.image = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)

priestess = Fighter(220, 130, "Priestess", 80, 30, 3)
bandit = Fighter(540, 230, "Bandit", 80, 25, 2)

run = True

while run:

    clock.tick(fps)
    draw_background()

    # draw fighters
    priestess.draw()
    bandit.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()