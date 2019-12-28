# bugs
# 1) look at prev_direction, if walking left, enemy to right of me dies
# 2) enemy is damaged too much, one shot kills some zombies

import pygame, time, random
black = (0,0,0)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
orange = (255,140,0)
screen_size = (1000,750)
game_over, start_game = False, True

class App:
    def __init__(self, args):
        self.bg = args
        self.bgCount = 0
        self.display_hp = False
        self.healthpack_delay = time.time()
        self.health_x = random_x = random.randint(50, screen_size[0]-50)
        self.health_y = y_coordinate = screen_size[1] - landon.walk_left[0].image.get_height()//2-10
        self.hp = get_healthpack(self.health_x, self.health_y)
        self.start_time = time.time()
        self.startCount = 0
        self.gun_damage = 34
        self.zombie_damage = 10
        self.allEnemies = []
        self.closest_enemy = None

    def start_screen(self):
        # bg = pygame.transform.scale(background[0], screen_size)
        screen.blit(landon.stand_left[Game.startCount//2].image, (landon.x,landon.y))
        self.startCount += 1
        self.startCount %= len(landon.stand_left)*2

    def check_zombie_damage(self, enemy):
        if enemy is self.closest_enemy:
            if landon.shoot and landon.shootCount == 2:
                if landon.left and enemy.x < landon.x:
                    enemy.health -= self.gun_damage
                elif landon.right and enemy.x > landon.x:
                    enemy.health -= self.gun_damage
                elif landon.look_left and enemy.x < landon.x:
                    enemy.health -= self.gun_damage
                elif landon.look_right and enemy.x > landon.x:
                    enemy.health -= self.gun_damage
            if enemy.health <= 0:
                enemy.dying = True

    def check_player_damage(self, enemy):
        distance_from_zombie = abs(landon.x - enemy.x)
        if enemy.attack and enemy.attackCount == 1:
            landon.health -= self.zombie_damage
        if landon.health <= 0:
            landon.dead = True

    def create_zombie(self):
        enemy = zombie()
        self.allEnemies.append(enemy)

    def find_closest_zombie(self):
        min_left = min_right = 1000
        left_index = right_index = -1
        for i, enemy in enumerate(self.allEnemies):
            if enemy.x < landon.x:
                if abs(landon.x-enemy.x) < min_left:
                    min_left = abs(landon.x-enemy.x)
                    left_index = i
            elif enemy.x > landon.x:
                if abs(landon.x-enemy.x) < min_right:
                    min_right = abs(landon.x-enemy.x)
                    right_index = i
        if landon.left or landon.look_left:
            if not left_index == -1:
                self.closest_enemy = self.allEnemies[left_index]
            else:
                self.closest_enemy = None
        elif landon.right or landon.look_right:
            if not right_index == -1:
                self.closest_enemy = self.allEnemies[right_index]
            else:
                self.closest_enemy = None

    def load_background(self):
        if landon.x+landon.width > screen_size[0]:
            landon.x = 0
            self.bgCount += 1
        elif landon.x < 0:
            landon.x = screen_size[0]-landon.width
            self.bgCount -= 1
        self.bgCount %= 4
        screen.blit(self.bg[self.bgCount], (0,0))

    def get_health_coordinates(self):
        self.health_x = random_x = random.randint(50, screen_size[0]-50)
        self.health_y = y_coordinate = screen_size[1] - landon.walk_left[0].image.get_height()//2-10
        self.hp.rect.topleft = (self.health_x, self.health_y)

    def draw_healthpack(self):
        keys = pygame.key.get_pressed()
        time_now = time.time()
        if time_now - self.healthpack_delay > 30:
            self.display_hp = True
        if self.display_hp:
            screen.blit(self.hp.image, (self.health_x, self.health_y))
        if pygame.sprite.collide_rect(self.hp, landon.current_sprite()) and keys[pygame.K_SPACE]:
            # print(self.hp.rect, landon.current_sprite().rect)
            landon.health += 25
            if landon.health > 100:
                landon.health = 100
            self.display_hp = False
            self.healthpack_delay = time.time()
            self.get_health_coordinates()

    def time_passed(self, seconds):
        time_now = time.time()
        if time_now - self.start_time >= seconds:
            self.start_time = time.time()
            return True
        return False

class player:
    def __init__(self):
        self.health = 100
        self.shoot = False
        self.left = self.right = False
        self.look_left, self.look_right = True, False
        self.dead = False
        self.walkCount = self.standCount = self.shootCount = self.dieCount = 0
        self.spritesheet = pygame.image.load('pictures/female main character.png').convert_alpha()
        self.sprites = self.get_character_sprites(8, 8)
        self.stand_left = self.sprites[0]
        self.stand_right = self.sprites[1]
        self.walk_left = self.sprites[2]
        self.walk_right = self.sprites[3]
        self.shoot_left = self.sprites[4]
        self.shoot_right = self.sprites[5]
        self.die_left = self.sprites[6]
        self.die_right = self.sprites[7]

        self.x,self.y = screen_size[0]//2, screen_size[1] - self.walk_left[0].image.get_height()
        self.width, self.height = self.walk_left[0].image.get_width(), self.walk_left[0].image.get_height()

    def get_character_sprites(self, row, col):
        sprites = []
        ss_width = self.spritesheet.get_width()//8
        ss_height = self.spritesheet.get_height()//8

        for r in range(row):
            sprite_row = []
            for c in range(col):
                sprite = pygame.sprite.Sprite()
                image = self.spritesheet.subsurface(c*ss_width,r*ss_height,ss_width,ss_height)
                sprite.image = image
                sprite.rect = image.get_rect()
                if self.character_sprite(image):
                    sprite_row.append(sprite)
            sprites.append(sprite_row)
        return sprites

    def character_sprite(self, image):
        width = image.get_width()
        height = image.get_height()
        for r in range(height):
            for c in range(width):
                if not image.get_at((r,c)) == (0,0,0,0):
                    return True
        return False

    def walk(self):
        if self.left:
            screen.blit(landon.walk_left[self.walkCount].image, (self.x,self.y))
        elif self.right:
            screen.blit(landon.walk_right[self.walkCount].image, (self.x,self.y))
        else:
            if landon.look_left:
                screen.blit(landon.stand_left[self.standCount//2].image, (self.x,self.y))
            elif landon.look_right:
                screen.blit(landon.stand_right[self.standCount//2].image, (self.x,self.y))

        if self.left or self.right:
            self.walkCount += 1
            self.walkCount %= len(landon.walk_left)
        else:
            self.standCount += 1
            self.standCount %= len(landon.stand_left)*2

    def fire_gun(self):
        if self.left or self.look_left:
            screen.blit(self.shoot_left[self.shootCount].image, (self.x,self.y))
        elif self.right or self.look_right:
            screen.blit(self.shoot_right[self.shootCount].image, (self.x,self.y))

        self.shootCount += 1
        self.shootCount %= len(self.shoot_left)
        if self.shootCount == 0:
            self.shoot = False

    def draw_health(self):
        width = self.width-40
        health_ratio = self.health/100
        health_color = green if self.health > 0 else red
        health_surface = pygame.Surface((width, 8))
        health_surface.fill((255,0,0))
        health_rect = pygame.Rect(0, 0, width*health_ratio, 8)
        pygame.draw.rect(health_surface, health_color, health_rect)
        screen.blit(health_surface, (self.x+20, self.y))

    def die(self):
        global game_over
        if self.left:
            screen.blit(self.die_left[self.dieCount//2].image, (self.x, self.y))
        elif self.right:
            screen.blit(self.die_right[self.dieCount//2].image, (self.x, self.y))
        elif self.look_left:
             screen.blit(self.die_left[self.dieCount//2].image, (self.x, self.y))
        elif self.look_right:
            screen.blit(self.die_right[self.dieCount//2].image, (self.x, self.y))

        self.dieCount += 1
        self.dieCount %= len(self.die_left)*2
        if self.dieCount == 0:
            game_over = True

    def current_sprite(self):
        sprite = pygame.sprite.Sprite()
        if self.left:
            sprite = self.walk_left[self.walkCount]
        elif self.right:
            sprite = self.walk_right[self.walkCount]
        elif self.look_left:
            sprite = self.stand_left[self.standCount//2]
        elif self.look_right:
            sprite = self.stand_right[self.standCount//2]
        # sprite.rect.move(self.x, self.y)
        sprite.rect.topleft = (self.x, self.y)
        return sprite

class zombie:
    def __init__(self):
        path = 'zombie_animations/Zombie1/'
        self.health = 100
        self.dead = self.dying = False
        self.width, self.height = 50,65
        self.walkCount = 0
        self.standCount = 0
        self.attackCount = 0
        self.dieCount = 0
        self.attack = False
        self.left = self.right = False
        self.walk_left = []
        self.walk_right = []
        self.attack_left = []
        self.attack_right = []
        self.die_left = []
        self.die_right = []
        self.idle = []

        for i in range(1,7):
            left_sprite = pygame.sprite.Sprite()
            right_sprite = pygame.sprite.Sprite()
            zombie = pygame.image.load(path+'Walk'+str(i)+'.png')
            resized_zombie = pygame.transform.scale(zombie, (self.width,self.height))
            left_sprite.image = pygame.transform.flip(resized_zombie, True, False)
            right_sprite.image = resized_zombie
            left_sprite.rect, right_sprite.rect = resized_zombie.get_rect(), resized_zombie.get_rect()
            self.walk_left.append(left_sprite)
            self.walk_right.append(right_sprite)
        for i in range(1, 5):
            sprite = pygame.sprite.Sprite()
            zombie = pygame.image.load(path+'Idle'+str(i)+'.png')
            resized_zombie = pygame.transform.scale(zombie, (self.width,self.height))
            sprite.image, sprite.rect = resized_zombie, resized_zombie.get_rect()
            self.idle.append(sprite)
        for i in range(1, 7):
            left_sprite = pygame.sprite.Sprite()
            right_sprite = pygame.sprite.Sprite()
            zombie = pygame.image.load(path+'Attack'+str(i)+'.png')
            resized_zombie = pygame.transform.scale(zombie, (self.width,self.height))
            left_sprite.image, right_sprite.image = pygame.transform.flip(resized_zombie, True, False), resized_zombie
            left_sprite.rect, right_sprite.rect = resized_zombie.get_rect(), resized_zombie.get_rect()
            self.attack_left.append(left_sprite)
            self.attack_right.append(right_sprite)
        for i in range(1,9):
            left_sprite = pygame.sprite.Sprite()
            right_sprite = pygame.sprite.Sprite()
            zombie = pygame.image.load(path+'Dead'+str(i)+'.png')
            resized_zombie = pygame.transform.scale(zombie, (round(zombie.get_width()*0.2),round(zombie.get_height()*0.2)))
            # print(zombie.get_width(), zombie.get_height())
            left_sprite.image, right_sprite.image = pygame.transform.flip(resized_zombie, True, False), resized_zombie
            left_sprite.rect = right_sprite.rect = resized_zombie.get_rect()

            self.die_left.append(left_sprite)
            self.die_right.append(right_sprite)
        start = random.randint(0,1)
        self.x = -10 if start == 0 else screen_size[0] + 10
        self.y = screen_size[1] - self.walk_left[0].image.get_height() - 15

    def find_direction(self):
        if abs(landon.x-(self.x-4)) < abs(landon.x-(self.x+4)):
            self.left = True
            self.right = False
        elif abs(landon.x-(self.x+4)) < abs(landon.x-(self.x-4)):
            self.left = False
            self.right = True
        else:
            self.left = False
            self.right = False

    def walk(self):
        self.find_direction()
        if self.left:
            self.x -= 4*int(not(self.attack))
            screen.blit(self.walk_left[self.walkCount//2].image, (self.x,self.y))
        elif self.right:
            self.x += 4*int(not(self.attack))
            screen.blit(self.walk_right[self.walkCount//2].image, (self.x,self.y))
        else:
            screen.blit(self.idle[self.standCount//2].image, (self.x,self.y))
        if self.left or self.right:
            self.walkCount += 1
            self.walkCount %= len(self.walk_left)*2
        else:
            self.standCount += 1
            self.standCount %= len(self.idle)*2

    def attack_player(self):
        if self.left:
            screen.blit(self.attack_left[self.attackCount//2].image, (self.x,self.y))
        elif self.right:
            screen.blit(self.attack_right[self.attackCount//2].image, (self.x,self.y))
        self.attackCount += 1
        self.attackCount %= len(self.attack_left)*2
        if self.attackCount == 0:
            self.attack = False
    def die(self):
        if self.left:
            screen.blit(self.die_left[self.dieCount//2].image, (self.x, self.y+self.die_left[0].image.get_height()-self.die_left[self.dieCount//2].image.get_height()))
        elif self.right:
            screen.blit(self.die_right[self.dieCount//2].image, (self.x, self.y+self.die_right[0].image.get_height()-self.die_right[self.dieCount//2].image.get_height()))
        self.dieCount += 1
        self.dieCount %= len(self.die_left)*2
        if self.dieCount == 0:
            self.dead = True
            self.dying = False

    def draw_health(self):
        health_ratio = self.health/100
        health_color = green if self.health > 0 else red
        health_surface = pygame.Surface((self.width, 8))
        health_surface.fill((255,0,0))
        health_rect = pygame.Rect(0, 0, self.width*health_ratio, 8)
        pygame.draw.rect(health_surface, health_color, health_rect)
        screen.blit(health_surface, (self.x, self.y-15))

    def current_sprite(self):
        sprite = pygame.sprite.Sprite()
        if self.left:
            sprite = self.walk_left[self.walkCount//2]
        elif self.right:
            sprite = self.walk_right[self.walkCount//2]
        else:
            sprite = self.idle[self.standCount//2]
        # sprite.rect.move(self.x, self.y)
        return sprite

def get_backgrounds():
    bg1 = pygame.image.load('pictures/bg1.png')
    bg2 = pygame.image.load('pictures/bg2.png')
    bg3 = pygame.image.load('pictures/bg3.png')
    bg4 = pygame.image.load('pictures/bg4.png')
    background1 = pygame.transform.scale(bg1, (1000,750))
    background2 = pygame.transform.scale(bg2, (1000,750))
    background3 = pygame.transform.scale(bg3, (1000,750))
    background4 = pygame.transform.scale(bg4, (1000,750))
    return background1, background2, background3, background4

def get_healthpack(health_x, health_y):
    hp = pygame.sprite.Sprite()
    image = pygame.image.load('pictures/healthpack1.png')
    image = pygame.transform.scale(image, (50, 50))
    hp.image = image
    hp.rect = image.get_rect(topleft=(health_x, health_y))
    return hp

pygame.init()
screen = pygame.display.set_mode(screen_size)
*backgrounds, = get_backgrounds()

# background = get_background_sprites(bg.get_width()//2, bg.get_height()//2, bg)

landon = player()
Game = App(backgrounds)
Game.create_zombie()

clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                landon.look_left, landon.look_right = False, False
                landon.left = True
                landon.right = False
                start_game = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                landon.look_left, landon.look_right = False, False
                landon.left = False
                landon.right = True
                start_game = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                landon.look_left, landon.look_right = True, False
                landon.left = landon.right = False
            elif event.key == pygame.K_RIGHT:
                landon.look_left, landon.look_right = False, True
                landon.left = landon.right = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            landon.shoot = True
            start_game = False

    if landon.left:
        landon.x -= 8*int(not(landon.shoot))
    elif landon.right:
        landon.x += 8*int(not(landon.shoot))

    Game.load_background()

    if Game.time_passed(5):
        Game.create_zombie()

    Game.find_closest_zombie()
    if not start_game:
        if landon.dead:
            landon.die()
            landon.left = landon.right = False
        else:
            if landon.shoot:
                landon.fire_gun()
            else:
                landon.walk()
        for enemy in Game.allEnemies:
            attack_distance = 15 if enemy.right else 65
            if abs(landon.x - enemy.x) < attack_distance:
                enemy.attack = True
            if not enemy.dying and not enemy.dead:
                Game.check_zombie_damage(enemy)
                if enemy.attack:
                    enemy.attack_player()
                else:
                    enemy.walk()
            elif enemy.dying:
                enemy.die()
            if not enemy.dead:
                enemy.draw_health()
            else:
                Game.allEnemies.remove(enemy)
            Game.check_player_damage(enemy)
            landon.draw_health()

        if len(Game.allEnemies) == 0:
            landon.draw_health()

    else:
        Game.start_screen()

    Game.draw_healthpack()
    clock.tick(16)
    pygame.display.update()

pygame.quit()
