import pygame
from pygame.locals import *
pygame.init()
import pickle
from os import path
from subprocess import call



screen_height = 600
screen_width = 800
lower_margin = 100
side_margin = 300
screen = pygame.display.set_mode((screen_width + side_margin, screen_height + lower_margin))

ROWS = 12
COLS = 16
tile_size = 50
tile_types = 12
current_tile = 0
selected_tile = 1
level = 0
level_num = str(level)
clock = pygame.time.Clock()
fps = 60

bg = pygame.image.load("Art/img_background.png")
img_list = []
for x in range(0, tile_types):
    img = pygame.image.load(f"Art/tiles/tile{x}.png")
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)
save_img = pygame.image.load("Art/save_btn.png")
load_img = pygame.image.load("Art/shop.png")
back_img = pygame.image.load("Art/back_btn.png")
back_img = pygame.transform.flip(back_img, True, False)


white = ((255, 255, 255))

font = pygame.font.SysFont("Courier New", 20, True)

world_data = []
for row in range(ROWS):
    r = [0] * COLS
    world_data.append(r)
for tile in range(0, COLS):
    world_data[ROWS - 1][tile] = 2
    world_data[0][tile] = 1
for row in range(ROWS):
    world_data[row][0] = 1
    world_data[row][COLS - 1] = 1

print(world_data)

def save_level():
    if level >= 1:
        pickle_out = open(f"level_data/main_levels/level{level}_data", "wb")
    else:
        pickle_out = open(f"level_data/level{level}_data", "wb")
    pickle.dump(world_data, pickle_out)
    pickle_out.close()
    print(world_data)

def load_level():
    no_level = True
    if level >= 1:
        if path.exists(f"level_data/main_levels/level{level}_data"):
            world_data = []
            pickle_in = open(f"level_data/main_levels/level{level}_data","rb")
            world_data = pickle.load(pickle_in)
            no_level = False
    else:
        if path.exists(f"level_data/level{level}_data"):
            world_data = []
            pickle_in = open(f"level_data/level{level}_data","rb")
            world_data = pickle.load(pickle_in)
            no_level = False
    if no_level:
        world_data = []
        for row in range(ROWS):
            r = [0] * COLS
            world_data.append(r)
        for tile in range(0, COLS):
            world_data[ROWS - 1][tile] = 2
            world_data[0][tile] = 1
        for row in range(ROWS):
            world_data[row][0] = 1
            world_data[row][COLS - 1] = 1

    return world_data

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_grid():
    for c in range(COLS + 1):
        pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height))
    for c in range(ROWS + 1):
        pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))

def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 1:
              screen.blit(img_list[tile - 1], (x * tile_size, y * tile_size))

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

save_button = Button(screen_width // 2, screen_height + lower_margin - 75, save_img, 100, 50)
load_button = Button(screen_width // 2 + 200, screen_height + lower_margin - 75, load_img, 100, 50)
back_button = Button(screen_width + side_margin - 35, 10, back_img, 25, 25)
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = Button(screen_width + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], tile_size, tile_size)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0
world_data = load_level()
if path.exists(f"unlocked"):
    pickle_in = open(f"unlocked","rb")
    run = pickle.load(pickle_in)
else:
    run = False
while run:
    clock.tick(fps)
    screen.fill((120,220,120))
    screen.blit(bg, (0,0))
    draw_grid()
    draw_world()

    draw_text(f"Level: {level_num}", font, white, 10, screen_height + lower_margin - 90)
    draw_text("Press Up or Down to change level", font, white, 10, screen_height + lower_margin - 70)

    if save_button.draw():
        save_level()
    if load_button.draw():
        world_data = load_level()
    #if back_button.draw():
    #    pygame.quit()
    #    call(["python", "pygametest.py"])
    #    run = False

    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw():
            current_tile = button_count
            selected_tile = button_count + 1

    pygame.draw.rect(screen, (255, 0, 0), button_list[current_tile].rect, 4)

    pos = pygame.mouse.get_pos()
    x = (pos[0]) // tile_size
    y = (pos[1]) // tile_size

    if pos[0] < screen_width and pos[1] < screen_height:
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != selected_tile:
                world_data[y][x] = selected_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = 0
    

    for event in pygame.event.get():  #Event handler
        if event.type == pygame.QUIT:
            #pygame.quit()
            #call(["python", "pygametest.py"])
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
                if level >= 0:
                    level_num = str(level)
                    world_data = load_level()
                elif level < 0:
                    level_num = (f"test_level{abs(level)}")
                    world_data = load_level()
                world_data = load_level()
            if event.key == pygame.K_DOWN:
                level -= 1
                if level >= 0:
                    level_num = str(level)
                    world_data = load_level()
                elif level < 0:
                    level_num = (f"test_level{abs(level)}")
                    world_data = load_level()
            

    pygame.display.update()

pygame.quit()