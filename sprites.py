import pygame as py
from settings import *
from os.path import isfile, join
from os import listdir


def flip(sprites):
    return [pg.transform.flip(sprite, True, False) for sprite in sprites]

#------------------------------------------------
def load_sprite_sheets(directory, width, height, sprite_scale):
    path = join("assets/sprites", directory)
    files = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for file in files:
        sprite_sheet = pg.image.load(join(path, file)).convert_alpha()
        #print(join(path, file)) # path er mappe retningen som er definert tidligere mens sprite er navnet på filen
        #print(sprite_sheet)

        sprites = []

        for i in range(sprite_sheet.get_width() // width):
            surface = pg.Surface((width, height), pg.SRCALPHA, 32)  # pygame.SRCALPHA gjør at man kan loade gjennomsiktig bakgrunn, 32 er farge dybden målt i bits
            rect = pg.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect) # blitter et utklipp av spritesheeten i posisjon (0,0) på surfacen
            sprites.append(pg.transform.scale_by(surface, sprite_scale)) # legger til og skalerer bildet i en liste av sprites

            all_sprites[file.replace(".png", "") + "_right"] = sprites
            all_sprites[file.replace(".png", "") + "_left"] = flip(sprites)

    return all_sprites


#------------------------------------------------

class Portal:
    def __init__(self, x, y):
        self.sprites = load_sprite_sheets("portal", 70, 100, PORTAL_SCALE)
        self.rect = self.sprites["portal_right"][0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.sprites["portal_right"][0].get_width()
        self.height = self.sprites["portal_right"][0].get_height()

        self.direction = "right"
        self.animation_count = 5

    def update_sprite(self):
        self.animation_count += 1

    def draw(self):
        SCREEN.blit(self.sprites["portal_right"][(self.animation_count // ANIMATION_DELAY) % len(self.sprites["portal_right"])], self.rect)


class Car:
    def __init__(self, x, y, directory):
        self.sprites = load_sprite_sheets(directory, 24, 12, CAR_SCALE)
        self.name = directory
        self.direction = "left"
        self.rect = self.sprites[self.name + "_" + self.direction][0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.sprites[self.name + "_" + self.direction][0].get_width()
        self.height = self.sprites[self.name + "_" + self.direction][0].get_height()
        self.hitbox = [[self.rect.x, self.rect.y + 12 * CAR_SCALE // 2.5, CAR_HITBOX, CAR_HITBOX], [self.rect.x + 24 * CAR_SCALE // 3, self.rect.y, CAR_HITBOX, CAR_HITBOX]]

        self.animation_count = 5

    def move(self):
        self.rect.x -= CAR_SPEED
        self.hitbox[0][0] -= CAR_SPEED
        self.hitbox[1][0] -= CAR_SPEED

    def update_sprite(self):
        self.animation_count += 1

    def draw(self):
        # pg.draw.rect(SCREEN, RED, self.hitbox[0])
        # pg.draw.rect(SCREEN, RED, self.hitbox[1])
        # pg.draw.rect(SCREEN, RED, self.rect)
        SCREEN.blit(self.sprites[self.name + "_" + self.direction][(self.animation_count // ANIMATION_DELAY) % len(self.sprites[self.name + "_" + self.direction])], self.rect)


class Truck:
    def __init__(self, x, y, directory):
        self.sprites = load_sprite_sheets(directory, 48, 36, CAR_SCALE)
        self.name = directory
        self.direction = "right"
        self.rect = self.sprites[self.name + "_" + self.direction][0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.sprites[self.name + "_" + self.direction][0].get_width()
        self.height = self.sprites[self.name + "_" + self.direction][0].get_height()
        self.animation_count = 5

    def move(self):
        self.rect.x += CAR_SPEED * 1.5

    def update_sprite(self):
        self.animation_count += 1

    def draw(self):
        # pg.draw.rect(SCREEN, RED, self.rect)
        SCREEN.blit(self.sprites[self.name + "_" + self.direction][(self.animation_count // ANIMATION_DELAY) % len(self.sprites[self.name + "_" + self.direction])], self.rect)


class Arne:
    def __init__(self, x, y):
        self.sprites = load_sprite_sheets("Arne", 5, 8, PLAYER_SCALE)
        self.rect = self.sprites["Arne_right"][0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.sprites["Arne_right"][0].get_width()
        self.height = self.sprites["Arne_right"][0].get_height()
        self.direction = "right"
        self.animation_count = 10
        self.walking = 0

    def update(self):
        if self.walking > 0:
            self.animation_count += 1
        self.rect.x += self.walking

    def draw(self):
        SCREEN.blit(self.sprites[f"Arne_{self.direction}"][(self.animation_count // ANIMATION_DELAY) % len(self.sprites[f"Arne_{self.direction}"])], self.rect)


class Player:
    def __init__(self, x, y):
        self.sprites = load_sprite_sheets("Didrik", 5, 8, PLAYER_SCALE)
        self.rect = self.sprites["didrik_walking_right"][0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.sprites["didrik_walking_right"][0].get_width()
        self.height = self.sprites["didrik_walking_right"][0].get_height()
        self.vel_y = 0

        self.current_animation = "didrik_walking"
        self.direction = "right"
        self.animation_count = 5

        self.jumped = False
        self.moving_x = False

        self.talking = False

        # print(self.sprites)


    def update(self, world):
        key = py.key.get_pressed()
        delta = [0, 0]
        self.current_animation = "didrik_chilling"

        if not self.talking:

            if (key[py.K_UP] or key[py.K_SPACE]) and self.jumped == False:
                self.vel_y = - JUMP_SPEED
                self.jumped = True


            if (key[py.K_UP] or key[py.K_SPACE]) == False and self.vel_y != 0:
                self.jumped = True

            if self.jumped:
                self.current_animation = "didrik_jumping"

            if key[py.K_LEFT] or key[py.K_a]:
                delta[0] -= WALKING_SPEED

                if not self.jumped:
                    self.current_animation = "didrik_walking"
                    self.direction = "left"
                    self.animation_count += 1

            if key[py.K_RIGHT] or key[py.K_d]:
                delta[0] += WALKING_SPEED

                if not self.jumped:
                    self.current_animation = "didrik_walking"
                    self.direction = "right"
                    self.animation_count += 1

        self.vel_y += GRAVITATIONAL_ACCELERATION
        if self.vel_y > TERMINAL_VELOCITY:
            self.vel_y = TERMINAL_VELOCITY
        delta[1] += self.vel_y

        #kollisjoner
        for tile in world.tile_list:
            # x
            if tile[1].colliderect(self.rect.x  + delta[0], self.rect.y, self.width, self.height):  # tile[0] er bildet
                delta[0] = 0
                self.moving_x = False
                self.current_animation = "didrik_chilling"

            # y
            if tile[1].colliderect(self.rect.x, self.rect.y + delta[1], self.width, self.height):
                if self.vel_y >= 0:  # sjekker om han står på bakken
                    delta[1] = tile[1].top - self.rect.bottom
                    self.jumped = False
                    self.vel_y = 0
                elif self.vel_y < 0:  # sjekker om han dunker hodet
                    delta[1] = tile[1].bottom - self.rect.top
                    self.vel_y = 0

            if self.rect.x < 0:
                self.rect.x = 0
                self.moving_x = False
                self.current_animation = "didrik_chilling"

            if self.rect.y < 0:
                self.rect.y = 0
                self.vel_y = 0

        self.rect.x += delta[0]
        self.rect.y += delta[1]



    def draw(self):
        # pg.draw.rect(SCREEN, (0, 0, 255), self.rect)

        SCREEN.blit(self.sprites[f"{self.current_animation}_{self.direction}"][(self.animation_count // ANIMATION_DELAY) % len(self.sprites[f"{self.current_animation}_{self.direction}"])], self.rect)
