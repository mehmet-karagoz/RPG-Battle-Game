import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
screen_width = 800
screen_height = 400

#game variables
current_fighter = 1
total_fighter = 2
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 30
clicked = False
game_over = 0

#fonts
font = pygame.font.SysFont("Times New Roman", 26)
font_potion = pygame.font.SysFont("Times New Roman", 15)

#colors
red = (255, 0, 0)
green = (0, 255, 0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("RPG Battle")

icon = pygame.image.load("img/Icons/rpg-game.png").convert_alpha()
pygame.display.set_icon(icon)

#load images
#background image
background_img = pygame.image.load("img/Background/background.png").convert_alpha()
potion_img = pygame.image.load("img/Potions/h0.png").convert_alpha()
sword_img = pygame.image.load("img/Icons/sword.png").convert_alpha()
victory_img = pygame.image.load("img/Icons/victory.png").convert_alpha()
defeat_img = pygame.image.load("img/Icons/defeat.png").convert_alpha()
restart_img = pygame.image.load("img/Icons/restart.png").convert_alpha()


# functions

#draw text
def draw(text, font, text_color, x ,y):
    img = font.render(text, True, text_color)
    screen.blit(img,( x, y))

#draw background
def draw_background():
    screen.blit(background_img, (0,0))

#classes
class Fighter():
    def __init__(self, x, y, name , max_hp, strength, potions):
        self.x = x
        self.y = y
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #Idle
        if self.name == "Priestess":
            range_num = 8
        else:
            range_num = 4
        temp_list = []
        for i in range(range_num):
            img = pygame.image.load(f"img/{self.name}/Idle/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Attack
        temp_list = []
        for i in range(7):
            img = pygame.image.load(f"img/{self.name}/Attack/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Hurt
        temp_list = []
        if self.name == "Priestess":
            range_num = 7
        else:
            range_num = 2
        for i in range(range_num):
            img = pygame.image.load(f"img/{self.name}/Hurt/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Death
        temp_list = []
        if self.name == "Priestess":
            range_num = 16
        else:
            range_num = 8
        for i in range(range_num):
            img = pygame.image.load(f"img/{self.name}/Death/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Heal
        temp_list = []
        for i in range(12):
            img = pygame.image.load(f"img/Priestess/Heal/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Walk
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f"img/Priestess/Walk/{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        distance = abs(self.rect.centerx - target.rect.centerx)
        if target.name == "Priestess":
            distance += 45
        if distance <= 179:
            rand = random.randint(-5, 5)
            damage = self.strength + rand
            target.hp -= damage
            target.hurt()
            if target.hp <= 0:
                target.alive = False
                target.death()
            #animate
            damage_text = Damage_Text(target.rect.centerx, target.rect.centery,str(damage), red)
            damage_text_group.add(damage_text)
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def heal(self):
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def walk(self):
        self.action = 5
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.frame_index = 0
        self.action = 0
        self.hp = self.max_hp
        self.update_time = pygame.time.get_ticks()
        self.rect.centerx = self.x
        self.rect.centery = self.y


    def draw(self):
        screen.blit(self.image, self.rect)


class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        img = pygame.image.load("img/Icons/health_bar.png")
        self.image = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, red, (self.x - 126, self.y - 5, 258 * ratio, 11))

class Damage_Text(pygame.sprite.Sprite):
    def __init__(self, x , y, damage , color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

damage_text_group = pygame.sprite.Group()

priestess = Fighter(220, 130, "Priestess", 80, 30, 3)
bandit = Fighter(540, 230, "Bandit", 80, 25, 2)

priestess_health_bar = HealthBar(200, 30, priestess.hp, priestess.max_hp)
bandit_health_bar = HealthBar(600, 30, bandit.hp, bandit.max_hp)

potion_button = button.Button(screen, 30, 300, potion_img, 32,32)
restart_button = button.Button(screen, 280, 300, restart_img, 220,60)

run = True

priestess_x_change = 0

while run:

    clock.tick(fps)
    draw_background()

    # draw fighters
    priestess.update()
    priestess.draw()
    bandit.update()
    bandit.draw()

    damage_text_group.update()
    damage_text_group.draw(screen)

    #fighter stats
    priestess_health_bar.draw(priestess.hp)
    bandit_health_bar.draw(bandit.hp)

    #control actions
    attack = False
    potion = False
    position = pygame.mouse.get_pos()
    pygame.mouse.set_visible(True)
    if bandit.rect.collidepoint(position):
        pygame.mouse.set_visible(False)

        screen.blit(sword_img, position)

        if clicked and bandit.alive:
            attack = True
    
    if potion_button.draw():
        potion = True
    draw(str(priestess.potions), font_potion, green, 63, 313)

    if game_over == 0:
        #attack 
        if priestess.alive:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    if attack:
                        priestess.attack(bandit)
                        current_fighter += 1
                        action_cooldown = 0
                    if potion:
                        if priestess.potions > 0:
                            if priestess.max_hp - priestess.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = priestess.max_hp - priestess.hp
                            priestess.hp += heal_amount
                            priestess.heal()
                            heal_text = Damage_Text(priestess.rect.centerx, priestess.rect.centery,str(heal_amount), green)
                            damage_text_group.add(heal_text)
                            priestess.potions -= 1
                            current_fighter += 1
                            action_cooldown = 0
        else:
            game_over = -1

        if bandit.alive:
            if current_fighter == 2:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    bandit.attack(priestess)
                    current_fighter += 1
                    action_cooldown = 0
        else:
            current_fighter += 1
            game_over = 1

        if current_fighter > total_fighter:
            current_fighter = 1
    
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (125, 50))
        else:
            screen.blit(defeat_img, (186, 40))
        if restart_button.draw():
            priestess.reset()
            bandit.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0

    priestess.rect.centerx += priestess_x_change

    if priestess.rect.centerx <= 85:
        priestess.rect.centerx = 85
    elif priestess.rect.centerx >= 478:
        priestess.rect.centerx = 478

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                priestess_x_change = -3
                priestess.walk()              
            if event.key == pygame.K_RIGHT:
                priestess_x_change = 3
                priestess.walk()
        else:
            priestess_x_change = 0
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()