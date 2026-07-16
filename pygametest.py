import pygame
from pygame.locals import *
from pygame import mixer
import pickle
import os
from os import path
from random import randint
import datetime
import signal

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

clock = pygame.time.Clock()
fps = 60

#we are the gladiators

#we both grow on cheese

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Adventures of Indi & Olive")
icon = pygame.image.load("C:/pygameplatformer/Art/cover.png")
pygame.display.set_icon(icon)

#SCREEN_WIDTH = screen.get_width()
#SCREEN_HEIGHT = screen.get_height()

selected_font = pygame.font.SysFont("Courier New", 23, True)
game_over_font = pygame.font.SysFont("Courier New", 70, True)
font_score = pygame.font.SysFont("Comic Sans MS", 30)

playerChar = 1
rows = 12
cols = 16
tile_height = SCREEN_HEIGHT//rows
tile_width = SCREEN_WIDTH//cols
game_over = 0
main_menu = 1
level = 1
max_levels = len(os.listdir("C:/pygameplatformer/level_data/main_levels"))
print(f"hello i like cheese! also a {max_levels} for good measure.")
score = 0
total_score = 0
selected = 1
no_data = False
today = datetime.datetime.now()
date = (today.strftime("%d") + "/" + today.strftime("%m") + "/" + today.strftime("%y"))
save_btn_spacing = 1
save_slot = 0
#crate_x = 0
#crate_y = 0

white = (255, 255, 255)
red = (255, 0, 0)

bg_img2 = pygame.image.load("C:/pygameplatformer/Art/backround2.png")
bg2 = pygame.transform.scale(bg_img2, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_img = pygame.image.load("C:/pygameplatformer/Art/img_background.png")
bg = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
restart_img = pygame.image.load("C:/pygameplatformer/Art/_restart_btn.png")
start_img = pygame.image.load("C:/pygameplatformer/Art/start_btn.png")
exit_img = pygame.image.load("C:/pygameplatformer/Art/exit_btn.png")
shop_img = pygame.image.load("C:/pygameplatformer/Art/shop.png")
back_img = pygame.image.load("C:/pygameplatformer/Art/back_btn.png")
olive_img = pygame.image.load("C:/pygameplatformer/Art/olive_btn.png")
indi_img = pygame.image.load("C:/pygameplatformer/Art/indi_btn.png")
save_img = pygame.image.load("C:/pygameplatformer/Art/save_btn.png")
load_img = pygame.image.load("C:/pygameplatformer/Art/load_btn.png")
fade_img = pygame.image.load("C:/pygameplatformer/Art/splash.png")
fade_img = pygame.transform.scale(fade_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

coin_sfx = pygame.mixer.Sound("C:/pygameplatformer/Art/collect_coin.wav")
coin_sfx.set_volume(0.5)
jump_sfx = pygame.mixer.Sound("C:/pygameplatformer/Art/jump.wav")
jump_sfx.set_volume(0.5)
game_over_sfx = pygame.mixer.Sound("C:/pygameplatformer/Art/death_sfx1.wav")
game_over_sfx.set_volume(0.5)
game_over_sfx2 = pygame.mixer.Sound("C:/pygameplatformer/Art/death_sfx2.wav")
game_over_sfx2.set_volume(0.5)
game_over_sfx3 = pygame.mixer.Sound("C:/pygameplatformer/Art/death_sfx3.wav")
game_over_sfx3.set_volume(0.5)

#def fade_img(img, duration, x, y):
#    for i in range(duration):
#        img.set_alpha((255 // duration) * i)
#        screen.blit(img, (x, y))
#        pygame.time.wait(100)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_level(level):
    player.reset(100, SCREEN_HEIGHT - 130)
    blob_group.empty()
    lava_group.empty()
    coin_group.empty()
    platform_group.empty()
    exit_group.empty()
    score_coin = Coin(tile_width // 2, tile_width // 2)
    coin_group.add(score_coin)
    crate_group.empty()
    conveyor_group.empty()
    #scaffold_group.empty()
    if level >= 1:
        if path.exists(f"C:/pygameplatformer/level_data/main_levels/level{level}_data"):
            pickle_in = open(f"C:/pygameplatformer/level_data/main_levels/level{level}_data", "rb")
            world_data = pickle.load(pickle_in)
            world = World(world_data)
    else:
        if path.exists(f"C:/pygameplatformer/level_data/level{level}_data"):
            pickle_in = open(f"C:/pygameplatformer/level_data/level{level}_data", "rb")
            world_data = pickle.load(pickle_in)
            world = World(world_data)

    return [world, world_data]

class Button():
    def __init__(self, x, y, image, size_x, size_y):
        btn_img = image
        self.image = pygame.transform.scale(btn_img, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, self.rect)
        if self.rect.collidepoint(pos):
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 4)

        return action

class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        speed = 5
        walk_cooldown = 5
        col_threshold = 20
        self.cratecollide = False
        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_sfx.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_a]:
                dx -= speed
                self.counter += 1
                self.direction = -1
            if key[pygame.K_d]:
                dx += speed
                self.counter += 1
                self.direction = 1
            
            if key[pygame.K_d] == False and key[pygame.K_a] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                
            self.vel_y += 1
            if self.vel_y > 50:
                self.vel_y = 50
            dy += self.vel_y

            self.in_air = True

            for platform in platform_group:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_threshold:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_threshold:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        self.vel_y = 1
                        dy = 0
                    if platform.move_x != 0 and abs((self.rect.bottom + dy) - platform.rect.top) < col_threshold:
                        self.rect.x += platform.move_direction
            
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

                for conveyor in conveyor_group:
                    if conveyor.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    if conveyor.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        if self.vel_y < 0:
                            dy = conveyor.rect.bottom - self.rect.top
                            self.vel_y = 0
                        elif self.vel_y >= 0:
                            dy = conveyor.rect.top - self.rect.bottom
                            self.vel_y = 0
                            self.in_air = False
                            dx += conveyor.move_direction

            for scaffold in world.scaffold_list:
                if scaffold[1].colliderect(self.rect.x, self.rect.y + dy + self.height + 5, self.width, 1):
                    if self.vel_y >= 0:
                        dy = scaffold[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            if pygame.sprite.spritecollide(self, blob_group, False) and self.in_air == False:
                game_over = -1
                if playerChar == 1:
                    rare_death = randint(1, 10)
                    if rare_death == 10:
                        game_over_sfx2.play()
                    else:
                        game_over_sfx.play()
                elif playerChar == 2:
                    game_over_sfx3.play()
            elif pygame.sprite.spritecollide(self, blob_group, True) and self.in_air:
                #blob_group.remove(blob)
                self.vel_y = -15
                        
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                if playerChar == 1:
                    rare_death = randint(1, 10)
                    if rare_death == 10:
                        game_over_sfx2.play()
                    else:
                        game_over_sfx.play()
                elif playerChar == 2:
                    game_over_sfx3.play()
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            #for platform in platform_group:
            #    if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
            #        dx = 0
            #    if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
            #        if abs((self.rect.top + dy) - platform.rect.bottom) < col_threshold:
            #            self.vel_y = 0
            #            dy = platform.rect.bottom - self.rect.top
            #        elif abs((self.rect.bottom + dy) - platform.rect.top) < col_threshold:
            #            self.rect.bottom = platform.rect.top - 1
            #            self.in_air = False
            #            self.vel_y = 1
            #            dy = 0
            #        if platform.move_x != 0 and abs((self.rect.bottom + dy) - platform.rect.top) < col_threshold:
            #            self.rect.x += platform.move_direction
            for crate in crate_group:  
                if crate.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):#pygame.sprite.spritecollide(self, crate_group, False)
                    self.cratecollide = True
                    for tile in world.tile_list:      
                        if tile[1].colliderect(crate.rect.x + dx, crate.rect.y, tile_width, tile_height):
                            dx = 0
                    #if crate.rect.colliderect(crate.rect.x + dx, crate.rect.y, tile_width, tile_height):
                    #        dx = 0
                    if crate.conveyorcollide:
                        for conveyor in conveyor_group:
                            dx = conveyor.move_direction
                    crate.rect.x += dx
                if crate.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = crate.rect.bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = crate.rect.top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
                
        

            self.rect.x += dx
            self.rect.y += dy

        if game_over == -1:
            self.image = self.dead_image
            draw_text("GAME OVER!", game_over_font, red, (SCREEN_WIDTH // 2) - 200, (SCREEN_HEIGHT // 2) - 70)
            if self.rect.y > 100:
                self.rect.y -= 5

        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        #self.dx = dx
        

        return game_over
    
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            if playerChar == 1:
                img_right = pygame.image.load(f"C:/pygameplatformer/Art/person{num}.png")
            elif playerChar == 2:
                img_right = pygame.image.load(f"C:/pygameplatformer/Art/olive{num}.png")
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        death_img = pygame.image.load("C:/pygameplatformer/Art/ghost.png")
        self.dead_image = pygame.transform.scale(death_img, (40, 80))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
        self.cratecollide = False

class World():
    def __init__(self, data):
        self.tile_list = []
        self.scaffold_list = []

        dirt = pygame.image.load("C:/pygameplatformer/Art/dirt.png")
        grass = pygame.image.load("C:/pygameplatformer/Art/grass1.png")
        scaffold_air = pygame.image.load("C:/pygameplatformer/Art/scaffold/scaffold1.png")
        scaffold = pygame.image.load("C:/pygameplatformer/Art/scaffold/scaffold0.png")
        scaffold_overlay = pygame.image.load("C:/pygameplatformer/Art/scaffold/overlay.png")
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt, (tile_width, tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass, (tile_width, tile_height))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_width, row_count * tile_height + 15)
                    blob_group.add(blob)
                if tile == 4:
                    lava = Lava(col_count * tile_width, row_count * tile_height + (tile_height // 2))
                    lava_group.add(lava)
                if tile == 5:
                    exit = Exit(col_count * tile_width, row_count * tile_height - tile_height // 2)
                    exit_group.add(exit)
                if tile == 6:
                    coin = Coin(col_count * tile_width + (tile_width // 2), row_count * tile_height + (tile_height // 2))
                    coin_group.add(coin)
                if tile == 7:
                    platform = Platform(col_count * tile_width, row_count * tile_height, 0, 1)
                    platform_group.add(platform)
                if tile == 8:
                    platform = Platform(col_count * tile_width, row_count * tile_height, 1, 0)
                    platform_group.add(platform)
                if tile == 9:
                    crate = Crate(col_count * tile_width, row_count * tile_height)
                    crate_group.add(crate)
                if tile == 10:
                    conveyor = Conveyor(col_count * tile_width, row_count * tile_height, 0)
                    conveyor_group.add(conveyor)
                if tile == 11:
                    conveyor = Conveyor(col_count * tile_width, row_count * tile_height, 1)
                    conveyor_group.add(conveyor)
                if tile == 12:
                    # img = pygame.transform.scale(scaffold, (tile_width, tile_height))
                    # img_rect = img.get_rect()
                    # img_rect.x = col_count * tile_width
                    # img_rect.y = row_count * tile_height
                    # tile = (img, img_rect)
                    # self.scaffold_list.append(tile)
                    # scaffold_g = Scaffold(col_count * tile_width, row_count * tile_height)
                    # scaffold_group.add(scaffold_g)
                    col = col_count
                    row = row_count
                    img = pygame.transform.scale(scaffold_air, (tile_width, tile_height))
                    overlay = 0
                    overlay_left = 0
                    overlay_right = 0
                    if len(world_data) >= row:
                        if len(world_data[1]) >= col:
                            if world_data[row+1][col] == 1 or world_data[row+1][col] == 2 or world_data[row+1][col] == 12:
                                img = pygame.transform.scale(scaffold, (tile_width, tile_height))
                            if world_data[row][col-1] == 1 or world_data[row][col-1] == 2 or world_data[row][col-1] == 12:
                                overlay_left = pygame.transform.scale(scaffold_overlay, (tile_width, tile_height))
                                overlay = 1
                            if world_data[row][col+1] == 1 or world_data[row][col+1] == 2 or world_data[row][col+1] == 12:
                                overlay_right = pygame.transform.flip(pygame.transform.scale(scaffold_overlay, (tile_width, tile_height)), True, False)
                                overlay = 1
                    img_rect = img.get_rect()
                    if overlay == 1:
                        if overlay_left != 0:
                            overlay_l_img = pygame.transform.scale(overlay_left, (tile_width, tile_height))
                            img.blit(overlay_l_img, img_rect)
                            img_rect = img.get_rect()
                        if overlay_right != 0:
                            overlay_r_img = pygame.transform.scale(overlay_right, (tile_width, tile_height))
                            img.blit(overlay_r_img, img_rect)
                            img_rect = img.get_rect()
                    
                    img_rect.x = col_count * tile_width
                    img_rect.y = row_count * tile_height
                    tile = (img, img_rect)
                    self.scaffold_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)
        for tile in self.scaffold_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (0, 0, 255), tile[1], 2)
        
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("C:/pygameplatformer/Art/slime.png")
        self.image = pygame.transform.scale(img, (tile_width, tile_height - 15))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
    
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("C:/pygameplatformer/Art/lava_unedited.png")
        self.image = pygame.transform.scale(img, (tile_width, tile_height // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.index1 = 0
        self.cool_down = 0
        self.frame_count = []   
        for num in range(1, 5):
            img = pygame.image.load(f"C:/pygameplatformer/Art/coin{num}.png")
            self.image = pygame.transform.scale(img, (tile_width // 2, tile_height // 2))
            self.frame_count.append(img)
        self.image = self.frame_count[self.index1]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.cool_down += 1
        if self.cool_down >= 10:
            self.index1 += 1
            self.cool_down = 0
            if self.index1 < len(self.frame_count):
                self.image = self.frame_count[self.index1]
            else:
                self.index1 = 0
                self.image = self.frame_count[self.index1]

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("C:/pygameplatformer/Art/platform.png")
        self.image = pygame.transform.scale(img, (tile_width, tile_height // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.move_x = move_x
        self.move_y = move_y
    
    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("C:/pygameplatformer/Art/exit_door.png")
        self.image = pygame.transform.scale(img, (tile_width, int(tile_height * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Crate(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("C:/pygameplatformer/Art/crate.png")
        self.image = pygame.transform.scale(img, (tile_width, tile_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.conveyorcollide = False
    
    def update(self):
        dy = 0
        dx = 0
        self.conveyorcollide = False
        self.vel_y += 1
        if self.vel_y > 50:
            self.vel_y = 50
        dy += self.vel_y
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, tile_width, tile_height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
            for conveyor in conveyor_group:
                if conveyor.rect.colliderect(self.rect.x, self.rect.y + dy, tile_width, tile_height):
                    if self.vel_y < 0:
                        dy = conveyor.rect.bottom - self.rect.top
                        self.vel_y = 0
                        self.conveyorcollide = True
                    elif self.vel_y >= 0:
                        dy = conveyor.rect.top - self.rect.bottom
                        self.vel_y = 0
                        if player.cratecollide == False:
                            dx += conveyor.move_direction
                            self.conveyorcollide = True
                        else:
                            self.conveyorcollide = False
                    
        self.rect.y += dy
        self.rect.x += dx
        

class Conveyor(pygame.sprite.Sprite):
    def __init__(self, x, y, move_direction):
        pygame.sprite.Sprite.__init__(self)
        self.index1 = 0
        self.cool_down = 0
        self.frame_count = []
        for num in range(1, 6):
            if move_direction == 1:
                num = abs(num-4)+1
            img = pygame.image.load(f"C:/pygameplatformer/Art/conveyor0/conveyor{num}.png")
            self.image = pygame.transform.scale(img, (tile_width, tile_height))
            self.frame_count.append(img)
            self.image = self.frame_count[self.index1]
        self.image = self.frame_count[self.index1]
        self.image = pygame.transform.scale(img, (tile_width, tile_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if move_direction == 0:
            self.move_direction = -1
        elif move_direction == 1:
            self.move_direction = 1
    
    def update(self):
        self.cool_down += 1
        if self.cool_down >= 1:
            self.index1 += 1
            self.cool_down = 0
            if self.index1 < len(self.frame_count):
                self.image = self.frame_count[self.index1]
                self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
            else:
                self.index1 = 0
            self.image = self.frame_count[self.index1]
            self.image = pygame.transform.scale(self.image, (tile_width, tile_height))

# class Scaffold(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         pygame.sprite.Sprite.__init__(self)
#         self.tile_list = []
#         col = x // tile_width
#         row = y // tile_height
#         img = pygame.image.load("C:/pygameplatformer/Art/scaffold/scaffold1.png")
#         overlay = 0
#         overlay_left = 0
#         overlay_right = 0
#         if len(world_data) >= row:
#             if len(world_data[1]) >= col:
#                 if world_data[row+1][col] == 1 or world_data[row+1][col] == 2 or world_data[row+1][col] == 12:
#                     img = pygame.image.load("C:/pygameplatformer/Art/scaffold/scaffold0.png")
#                 if world_data[row][col-1] == 1 or world_data[row][col-1] == 2 or world_data[row][col-1] == 12:
#                     overlay_left = pygame.image.load("C:/pygameplatformer/Art/scaffold/overlay.png")
#                     overlay = 1
#                 if world_data[row][col+1] == 1 or world_data[row][col+1] == 2 or world_data[row][col+1] == 12:
#                     overlay_right = pygame.transform.flip(pygame.image.load("C:/pygameplatformer/Art/scaffold/overlay.png"), True, False)
#                     overlay = 1
#         self.image = pygame.transform.scale(img, (tile_width, tile_height))
#         self.rect = self.image.get_rect()
#         if overlay != 0:
#             if overlay_left != 0:
#                 overlay_l_img = pygame.transform.scale(overlay_left, (tile_width, tile_height))
#                 self.image.blit(overlay_l_img, self.rect)
#             if overlay_right != 0:
#                 overlay_r_img = pygame.transform.scale(overlay_right, (tile_width, tile_height))
#                 self.image.blit(overlay_r_img, self.rect)
            
        
#         self.rect.x = x
#         self.rect.y = y
            


player = Player(100, SCREEN_HEIGHT - 130)
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
score_coin = Coin(tile_width // 2, tile_width // 2)
coin_group.add(score_coin)
crate_group = pygame.sprite.Group()
conveyor_group = pygame.sprite.Group()
#scaffold_group = pygame.sprite.Group()
if path.exists(f"C:/pygameplatformer/level_data/main_levels/level{level}_data"):
    pickle_in = open(f"C:/pygameplatformer/level_data/main_levels/level{level}_data", "rb")
    world_data = pickle.load(pickle_in)
    world = World(world_data)
else:
    world_data = []
    for row in range(rows):
        r = [0] * cols
        world_data.append(r)
    for tile in range(0, cols):
        world_data[rows - 1][tile] = 2
        world_data[0][tile] = 1
    for row in range(rows):
        world_data[row][0] = 1
        world_data[row][cols - 1] = 1
    reset_level(level)[0]
world = World(world_data)
restart_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 30, restart_img, 125, 50)
start_button = Button(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 150, start_img, 200, 100)
exit_button = Button(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - 150, exit_img, 200, 100)
shop_button = Button(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2, shop_img, 200, 100)
back_button = Button(25 // 2, 25 // 2, back_img, 25, 25)
olive_button = Button(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2, olive_img, 200, 100)
indi_button = Button(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2, indi_img, 200, 100)
save_button = Button(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2, save_img, 200, 100)
save_num = len(os.listdir("C:/pygameplatformer/save_data"))
save_button_list = []
for i in range(save_num):
    save_btn = Button(SCREEN_WIDTH // 2 - 100, 125 * save_btn_spacing + 50, save_img, 200, 100)
    save_button_list.append(save_btn)
    save_btn_spacing += 1

new_save_button = Button(SCREEN_WIDTH // 2 - 100, 50, shop_img, 200, 100)
load_button = Button(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2, load_img, 200, 100)
editor_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, shop_img, 200, 100)

splash_screen = 0
music_init = True
fade_counter = 0
fade_out = False

pygame.time.wait(3000)

run = True
while run:

    key = pygame.key.get_pressed()

    clock.tick(fps)

    screen.fill((0,0,0))

    if splash_screen <= 7*30:   #Splash Screen
        if fade_counter <= 1*30 and fade_out == False:
            fade_img.set_alpha(int(255 / (1*30) * fade_counter))
            fade_counter += 1
        if splash_screen == 5*30 and fade_out == False:
            fade_out = True
            fade_counter = 0
        if fade_counter <= 1*30 and fade_out:
            fade_img.set_alpha(int(255 - (255 / (1*30) * fade_counter)))
            fade_counter += 1
        screen.blit(fade_img, (0,0))
        splash_screen += 1
        #print(fade_img.get_alpha())

    else:
        if music_init == True:
            pygame.mixer.music.load("C:/pygameplatformer/Art/bg_sfx.wav")
            pygame.mixer.music.play(-1, 0.0, 5000)
            music_init = False
        if main_menu >= 1:
            screen.blit(bg2, (0, 0))
        if main_menu == 1:
            shop_button = Button(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2, shop_img, 200, 100)
            save_button = Button(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2, save_img, 200, 100)
            if shop_button.draw():
                selected_text = draw_text("S E L E C T E D", selected_font, white, SCREEN_WIDTH // 2 - 255, SCREEN_HEIGHT // 2 + 110)
                main_menu = 2
                selected_text
            if exit_button.draw():
                run = False
                os.kill(os.getppid(), signal.SIGTERM)
            if start_button.draw():
                reset_level(level)[0]
                player.reset(100, SCREEN_HEIGHT - 130)
                score = 0
                main_menu = 0
            if save_button.draw():
                main_menu = 3
            #if editor_button.draw():
            #    pygame.quit()
            #    call(["python", "level_editor.py"])
            #    run = False
        elif main_menu == 2:
            selected = playerChar
            if back_button.draw():
                main_menu = 1
            if olive_button.draw():
                playerChar = 2
                selected = 2
            if selected == 2:
                selected_text = draw_text("S E L E C T E D", selected_font, white, SCREEN_WIDTH // 2 + 45, SCREEN_HEIGHT // 2 + 110)
            if indi_button.draw():
                playerChar = 1
                selected = 1
            if selected == 1:
                selected_text = draw_text("S E L E C T E D", selected_font, white, SCREEN_WIDTH // 2 - 255, SCREEN_HEIGHT // 2 + 110)
        elif main_menu == 3:
            if back_button.draw():
                main_menu = 1
            save_counter = 0
            for save_counter, s in enumerate(save_button_list):
                if s.draw():
                    save_slot = save_counter + 1
                    main_menu = 4
            if new_save_button.draw():
                level = 1
                world_data = reset_level(level)[1]
                world = reset_level(level)[0]
                game_over = 0
                score = 0
                player.reset(100, SCREEN_HEIGHT - 130)
                main_menu = 0
                save_data = [level, total_score, playerChar, date, save_num]
                export_data = open(f"save_data/save{save_num + 1}_data", "wb")
                pickle.dump(save_data, export_data)
                export_data.close()
                save_num = len(os.listdir("save_data"))

        elif main_menu == 4:
            if save_button.draw():
                save_data = [level, total_score, playerChar, date, save_num]
                export_data = open(f"save_data/save{save_slot}_data", "wb")
                pickle.dump(save_data, export_data)
                export_data.close()
                loaded_data = open(f"save_data/save{save_slot}_data", "rb")
                recovered_data = pickle.load(loaded_data)
                draw_text("Last Saved: " + recovered_data[3], selected_font, white, SCREEN_WIDTH // 2 - 255, SCREEN_HEIGHT // 2 + 110)
            if load_button.draw():
                if path.exists(f"save_data/save{save_slot}_data"):
                    loaded_data = open(f"save_data/save{save_slot}_data", "rb")
                    recovered_data = pickle.load(loaded_data)
                    level = recovered_data[0]
                    total_score = recovered_data[1]
                    playerChar = recovered_data[2]
                    main_menu = 0
                else:
                    no_data = True
                world_data = reset_level(level)[1]
                world = reset_level(level)[0]
            if no_data:
                draw_text("No Save Data!", game_over_font, white, SCREEN_WIDTH // 2 - 265, SCREEN_HEIGHT // 2 - 70)
            loaded_data = open("save_data/save1_data", "rb")
            recovered_data = pickle.load(loaded_data)
            draw_text("Last Saved: " + recovered_data[3], selected_font, white, SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 110)
                
            if back_button.draw():
                main_menu = 1
                no_data = False
                wait = 0
        elif main_menu == 0:
            screen.blit(bg, (0, 0))
            world.draw()
            if game_over == 0:
                blob_group.update()
                platform_group.update()
                if pygame.sprite.spritecollide(player, coin_group, True):
                    score += 1
                    coin_sfx.play()
            conveyor_group.draw(screen)
            conveyor_group.update()
            crate_group.draw(screen)
            crate_group.update()
            blob_group.draw(screen)
            lava_group.draw(screen)
            coin_group.draw(screen)
            coin_group.update()
            platform_group.draw(screen)
            #scaffold_group.draw(screen)
            exit_group.draw(screen)
            
            #crate_group.update()
            draw_text("X " + str(score + total_score), font_score, white, tile_width - 10, 3)
            game_over = player.update(game_over)
            #print(player.dx)
            if key[pygame.K_ESCAPE] and game_over != -1:
                main_menu = 1

            if game_over == -1:
                if restart_button.draw():
                    world_data = reset_level(level)[1]
                    world = reset_level(level)[0]
                    game_over = 0
                    score = 0
            if game_over == 1:
                level += 1
                if level <= max_levels:
                    world_data = reset_level(level)[1]
                    world = reset_level(level)[0]
                    game_over = 0
                    total_score += score
                    score = 0
                else:
                    draw_text("YOU WIN!", game_over_font, red, (SCREEN_WIDTH // 2)- 150, (SCREEN_HEIGHT // 2) - 70)
                    if restart_button.draw():
                        level = 1
                        world_data = reset_level(level)[1]
                        world = reset_level(level)[0]
                        game_over = 0
                        total_score += score
                        score = 0
                    pickle_out = open(f"unlocked", "wb")
                    pickle.dump(True, pickle_out)
                    pickle_out.close()

    for event in pygame.event.get():  #Event handler
        if event.type == pygame.QUIT:
            #pygame.quit()
            #sys.exit()
            pygame.mixer.stop()
            pygame.display.set_mode((0,0))
            run = False
            

    pygame.display.update()

pygame.quit()