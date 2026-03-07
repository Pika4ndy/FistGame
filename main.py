"""
Encore à faire :
    le rect de collision avec le joueur
    les effets de collisions sur le joueur(repulsion, changement d'anim avec le hit, ...)
    les vies du joueur
    les attaques du joueur pour combattre l'ennemi
"""
import pyscroll
import pytmx.util_pygame
import pygame

pygame.init()
BACKGROUND = pygame.Surface((640, 480))
SIZE = BACKGROUND.get_size()
FPS = 60

class Entity(pygame.sprite.Sprite):
    def __init__(self, sort, name, life, point_pos):
        super().__init__()
        # images (si ennemy : juste run et idle)
        self.type = sort
        if sort == "Heroes" or sort == "heroes":
            self.idle =[
                pygame.image.load(f"images/Heroes/{name}/{name}_m/{name}_m_idle_anim/{name}_m_idle_1.png"),
                pygame.image.load(f"images/Heroes/{name}/{name}_m/{name}_m_idle_anim/{name}_m_idle_2.png"),
                pygame.image.load(f"images/Heroes/{name}/{name}_m/{name}_m_idle_anim/{name}_m_idle_3.png"),
                pygame.image.load(f"images/Heroes/{name}/{name}_m/{name}_m_idle_anim/{name}_m_idle_4.png")
            ]

            self.idle_l=[pygame.transform.flip(image, 1, 0) for image in self.idle]

            self.run = [
                pygame.image.load(f"images/Heroes/{name}/{name}_M/{name}_m_run_anim/{name}_m_run_1.png"),
                pygame.image.load(f"images/Heroes/{name}/{name}_M/{name}_m_run_anim/{name}_m_run_2.png"),
                pygame.image.load(f"images/Heroes/{name}/{name}_M/{name}_m_run_anim/{name}_m_run_3.png"),
                pygame.image.load(f"images/Heroes/{name}/{name}_M/{name}_m_run_anim/{name}_m_run_4.png")
            ]

            self.run_l = [pygame.transform.flip(image, 1, 0) for image in self.run]

            self.hit = [
                pygame.image.load(f"images/Heroes/{name}/{name}_M/{name}_m_hit_anim/{name}_m_hit_1.png")
            ]
            self.hit_l=[pygame.transform.flip(image, 1, 0) for image in self.hit]

            self.stand = [pygame.image.load(f"images/Heroes/{name}/{name}_M/{name}_M.png")]

            self.sleep = []
            try:
                self.sleep = [
                    pygame.image.load(f"images/Heroes/{name}/{name}_M/{name}_m_sleep_anim/{name}_m_sleep_1.png"),
                    pygame.image.load(f"images/Heroes/{name}/{name}_M/{name}_m_sleep_anim/{name}_m_sleep_2.png"),
                    pygame.image.load(f"images/Heroes/{name}/{name}_M/{name}_m_sleep_anim/{name}_m_sleep_3.png"),
                    pygame.image.load(f"images/Heroes/{name}/{name}_M/{name}_m_sleep_anim/{name}_m_sleep_4.png")
                ]

                self.sleep_l=[pygame.transform.flip(image, 1, 0) for image in self.sleep]
            except:
                self.sleep = []

        else :
            self.idle =[
                pygame.image.load(f"images/{sort}/{name}/{name}_idle_anim/{name}_idle_1.png"),
                pygame.image.load(f"images/{sort}/{name}/{name}_idle_anim/{name}_idle_2.png"),
                pygame.image.load(f"images/{sort}/{name}/{name}_idle_anim/{name}_idle_3.png"),
                pygame.image.load(f"images/{sort}/{name}/{name}_idle_anim/{name}_idle_4.png")
            ]

            self.idle_l=[pygame.transform.flip(image, 1, 0) for image in self.idle]

            self.run = [
                pygame.image.load(f"images/{sort}/{name}/{name}_run_anim/{name}_run_1.png"),
                pygame.image.load(f"images/{sort}/{name}/{name}_run_anim/{name}_run_2.png"),
                pygame.image.load(f"images/{sort}/{name}/{name}_run_anim/{name}_run_3.png"),
                pygame.image.load(f"images/{sort}/{name}/{name}_run_anim/{name}_run_4.png"),
            ]
            self.run_l = [pygame.transform.flip(image, 1, 0) for image in self.run]

            self.stand = [pygame.image.load(f"images/{sort}/{name}/{name}.png")]


        self.current_sprite = 0
        self.image = self.idle[self.current_sprite]
        self.rect = self.image.get_rect()
        self.position = [point_pos.x, point_pos.y]
        self.rect.center = tuple(self.position)
        self.old_position = self.position.copy()
        self.is_right = True
        self.life = life
        self.feet = None
        if sort == "Heroes" or sort == "heroes":
            self.feet = pygame.Rect(0, 0, self.rect.width*3/4, 7)

    def animate(self, animation, speed):
        self.current_sprite += speed

        if self.current_sprite >= len(animation):
            self.current_sprite = 0

        self.image = animation[int(self.current_sprite)]

    def update(self):
        self.rect.center = tuple(self.position)
        if self.type == "heroes" and self.feet is not None:
            self.feet.midbottom = self.rect.midbottom


    def move_back(self):
        self.position = self.old_position
        self.rect.center = tuple(self.position)
        if self.type == "heroes" and self.feet is not None:
            self.feet.midbottom = self.rect.midbottom

class Knight(Entity):
    def __init__(self):
        self.point = tmxdata.get_object_by_name("player")
        super().__init__("Heroes", "knight", 150, self.point)
        self.feet = pygame.Rect(0, 0, self.rect.width*3/4, 7)

        self.is_right = True
        self.time = 0

    def save_location(self): 
        self.old_position = self.position.copy()

    def move_right(self, speed): self.position[0] += speed

    def move_left(self, speed): self.position[0] -= speed

    def move_up(self, speed): self.position[1] -= speed * 2/3

    def move_down(self, speed): self.position[1] += speed * 2/3

    def idle_animation(self):
        if self.is_right:
            self.animate(self.idle, 0.1)
            if not self.sleep == []:
                if current_time - self.time > 30000:
                    self.animate(self.sleep, 0.05)
            else:
                pass
        else:
            self.animate(self.idle_l, 0.1)
            if not self.sleep_l == []:
                if current_time - self.time > 30000:
                    self.animate(self.sleep_l, 0.05)
            else:
                pass
        

class Demons(Entity):
    def __init__(self,name):
        self.point = tmxdata.get_object_by_name("ennemy1")
        super().__init__("Demons", name, 50, self.point)
        
    def idle_animation(self):
        self.animate(self.idle, 0.075)
        

def handle_input(player, speed):
    pressed = pygame.key.get_pressed()
    

    if pressed[pygame.K_UP]:
        player.move_up(speed)
        player.time = 0
        if pressed[pygame.K_RIGHT]:
            pass
        if pressed[pygame.K_LEFT]:
            pass
        else:
            if player.is_right == True:
                knight.animate(player.run, 0.1)
            else:
                knight.animate(player.run_l, 0.1)

    if pressed[pygame.K_DOWN]:
        player.move_down(speed)
        player.time = 0
        if pressed[pygame.K_RIGHT]:
            pass
        if pressed[pygame.K_LEFT]:
            pass
        else:
            if player.is_right == True:
                knight.animate(player.run, 0.1)
            else:
                knight.animate(player.run_l, 0.1)

    if pressed[pygame.K_LEFT]:
        player.move_left(speed)
        player.time = 0
        knight.animate(player.run_l, 0.1)
        player.is_right = False

    if pressed[pygame.K_RIGHT]:
        player.move_right(speed)
        player.time = 0
        knight.animate(player.run, 0.1)
        player.is_right = True

    if sum(pressed) == 0:
        player.idle_animation()
        if player.time == 0:
            player.time = pygame.time.get_ticks()

def ennemies_input():
    for ennemy in ennemies:
        ennemy.idle_animation()

def update():
    group.update()
    ennemies_input()
    handle_input(knight, 2)

    for wall in walls:
        for player in players:
            if player.feet.colliderect(wall):
                player.move_back()



# initialisation de la fenetre
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Andy's game")
iconimg = pygame.image.load("images/sword.png")
pygame.display.set_icon(iconimg)

# init du clock
clock = pygame.time.Clock()
current_time = 0

# init de la carte

level1 = "Maps/level1.tmx"
current_map = level1
tmxdata = pytmx.util_pygame.load_pygame(current_map)
map_data = pyscroll.TiledMapData(tmxdata)
map_layer = pyscroll.orthographic.BufferedRenderer(map_data, screen.get_size())
map_layer.zoom = 2

walls = []
for obj in tmxdata.objects:
    if obj.name == "collision":
        walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    # init des points d'apparition
dict = {}


# init des entités
group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer = 3)
knight = Knight()
group.add(knight)
players = []
players.append(knight)
ennemy1 = Demons("chort")
ennemies = []
ennemies.append(ennemy1)
group.add(ennemy1)


# print here
# print()


run = True

while run:
    group.draw(screen)    

    knight.save_location()
    update()

    group.center(knight.rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    current_time = pygame.time.get_ticks()

    pygame.display.flip()
    clock.tick(FPS)

    group.clear(screen, BACKGROUND)

pygame.quit()