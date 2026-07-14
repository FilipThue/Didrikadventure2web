# Tutorial for å forstå tiles: https://www.youtube.com/watch?v=Ongc4EVqRjo

import pygame
import asyncio
from settings import *
from sprites import *

pygame.init()
font = pg.font.Font("assets/font/Grand9KPixel.ttf", 40)

pygame.display.set_caption("Didrik Adventure 2")

damage = None
music = None
pass

timer = [0, 0, 0]



class World:
    def __init__(self, data, lives):
        self.tile_list = []
        self.lives = lives

        self.checkpoint_life_img = py.transform.scale(checkpoint_life_img, (16 * LIFE_SCALE, 10 * LIFE_SCALE))
        self.one_life_img = py.transform.scale(one_life_img, (16 * LIFE_SCALE, 10 * LIFE_SCALE))

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                img = None
                if tile == 1:
                    img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))
                elif tile == 2:
                    img = pygame.transform.scale(ground_img, (TILE_SIZE, TILE_SIZE))
                if img:
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    self.tile_list.append((img, img_rect))

                col_count += 1
            row_count += 1

    def update(self):
        if self.lives < 0:
            print("Du er død")

    def draw(self):
        for tile in self.tile_list:
            SCREEN.blit(tile[0], tile[1])
            # pygame.draw.rect(SCREEN, (255, 255, 255), tile[1], 1)
        if self.lives > 0:
            SCREEN.blit(self.checkpoint_life_img, LIFE_POSITION)
        if self.lives == 0:
            SCREEN.blit(self.one_life_img, LIFE_POSITION)


class Game:
    def __init__(self, start_scene):
        self.scene = start_scene

    async def run(self):
        run = True
        clock = pg.time.Clock()

        while run:
            clock.tick(FPS)

            next_scene = self.scene.update()
            if next_scene:
                self.scene = next_scene

            self.scene.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()

            await asyncio.sleep(0)


# /------------------------------------------------------

class Prop:
    def __init__(self, x, y, w, h, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = pygame.transform.scale(img, (w, h))

    def draw(self):
        SCREEN.blit(self.img, (self.x, self.y))


class Spike:
    def __init__(self, x, y):
        self.img = pygame.transform.scale(spike_img, (TILE_SIZE, TILE_SIZE))
        self.x = x
        self.y = y
        self.hitbox = [x + SPIKE_LENIENCY / 2, y + SPIKE_LENIENCY, TILE_SIZE - SPIKE_LENIENCY,
                       TILE_SIZE - SPIKE_LENIENCY]

    def draw(self):
        SCREEN.blit(self.img, (self.x, self.y))
        # pygame.draw.rect(SCREEN, RED, self.hitbox, 2)


class Speech_bubble:
    def __init__(self, x, y, person, text):
        self.img = pg.image.load('assets/img/speech.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (80 * BUBBLE_SIZE, 60 * BUBBLE_SIZE))

        if person == "Arne":
            self.img = pg.transform.flip(self.img, True, False)

        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.text = text

    def draw(self):
        SCREEN.blit(self.img, (self.x, self.y))
        if type(self.text) == list:
            draw_text(self.text[0], font, BLACK, SCREEN, self.x + self.width // 2, self.y + self.height // 3)
            draw_text(self.text[1], font, BLACK, SCREEN, self.x + self.width // 2, self.y + (self.height // 4) * 2 )
        else:
            draw_text(self.text, font, BLACK, SCREEN, self.x + self.width // 2, self.y + self.height // 2)


# /------------------------------------------------------


class Scene:
    def update(self):
        return self

    def draw(self):
        pass


class Level_scene(Scene):
    def __init__(self, world_d, player_pos, lives, timer):
        self.world = World(world_d, lives)
        self.player = Player(player_pos[0], player_pos[1])
        self.lives = lives
        self.timer = timer

    def common_update(self):
        self.world.update()
        self.player.update(self.world)

        self.timer[0] += 1

        if self.timer[0] == 60:
            self.timer[1] += 1
            self.timer[0] = 0

        if self.timer[1] == 60:
            self.timer[2] += 1
            self.timer[1] = 0

        if self.timer[2] >= 5:
            self.lives = -1




    def draw(self):
        self.world.draw()
        draw_text(f"{4 - self.timer[2]} min {59 - self.timer[1]} sec", font, WHITE, SCREEN, TILE_SIZE * 1.1 , 0, True)


class Level5(Level_scene):
    def __init__(self, lives, timer):
        super().__init__(world_data_5, START_POS, lives, timer)

    def common_update(self):
        self.world.update()
        self.player.update(self.world)

    def update(self):
        self.common_update()

        if self.player.rect.x > WIDTH:
            return Start_screen()
        if self.lives < 0:
            return Loose_screen()

    def draw(self):
        SCREEN.blit(bg_img_level5, (0, 0))
        draw_text(f"Gratulerer, du rakk timen!", font, GOLD, SCREEN, WIDTH // 2, TILE_SIZE // 1.5)
        draw_text(f"Du hadde {4 - self.timer[2]} minutter og {59 - self.timer[1]},{self.timer[0]*6//10} sekunder til gode", font, GOLD, SCREEN, WIDTH // 2, HEIGHT // 4)
        draw_text(f"Start på nytt", font, WHITE, SCREEN, WIDTH - (TILE_SIZE * 3), HEIGHT - (TILE_SIZE * 4.5))
        SCREEN.blit(pil, (WIDTH - (TILE_SIZE * 4), HEIGHT - (TILE_SIZE * 4)))
        self.player.draw()
        self.world.draw()


class Level4(Level_scene):
    def __init__(self, lives, timer):
        super().__init__(world_data_4, START_POS, lives, timer)
        self.cars = [Car(WIDTH // 2, HEIGHT - TILE_SIZE - 12 * CAR_SCALE, "car"),
                     Car(WIDTH // 2 + CAR_SPACING, HEIGHT - TILE_SIZE - 12 * CAR_SCALE, "cabriolet"),
                     Car(WIDTH // 2 + CAR_SPACING + CAR_SPACING, HEIGHT - TILE_SIZE - 12 * CAR_SCALE, "cabriolet")]
        self.truck = Truck(-5090, HEIGHT - TILE_SIZE - 36 * CAR_SCALE, "lorry")
        self.Arne = Arne(-50, HEIGHT - TILE_SIZE - 8 * PLAYER_SCALE)
        self.arne_activate = False
        self.speech_bubbles = [Speech_bubble(ARNE_TALKING, HEIGHT // 4, "Arne", "Halla mann!"),
                               Speech_bubble(DIDRIK_TALKING, HEIGHT // 4, "Didrik", "Skjer a' Arne??"),
                               Speech_bubble(ARNE_TALKING, HEIGHT // 4, "Arne", ["Bare ute og", "jogger en tur"]),
                               Speech_bubble(ARNE_TALKING, HEIGHT // 4, "Arne", ["Må jo oprettholde", "Strava-streaken ;)"]),
                               Speech_bubble(DIDRIK_TALKING, HEIGHT // 4, "Didrik", ["Personlig foretrekker", "jeg disc golf"]),
                               Speech_bubble(DIDRIK_TALKING, HEIGHT // 4, "Didrik",["Fikk startet sesongen", "nå i påsken"]),
                               Speech_bubble(ARNE_TALKING, HEIGHT // 4, "Arne",["Har du retta noen", "prøver i det siste?"]),
                               Speech_bubble(DIDRIK_TALKING, HEIGHT // 4, "Didrik",["Skal høre en it-", "presentasjon 08:15"]),
                               Speech_bubble(DIDRIK_TALKING, HEIGHT // 4, "Didrik", ["Kan ikke stå her i veien", "og snakke dessverre"]),
                               Speech_bubble(DIDRIK_TALKING, HEIGHT // 4, "Didrik", "Må stikke, sneiksss! :)")]
        self.new_bubble_timer = 0
        self.bubble_count = 0
        self.pressed = False
        self.timer = timer

    def update(self):
        self.common_update()
        self.Arne.update()
        for car in self.cars:
            car.move()
            car.update_sprite()

            for hitbox in car.hitbox:
                if self.player.rect.colliderect(hitbox):
                    pass
                    if self.lives == 1:
                        return Level4(self.lives, self.timer)
                    else:
                        return Loose_screen()

        # Arne
        if self.player.rect.x > WIDTH // 2 and self.arne_activate == False:
            self.arne_activate = True
            self.Arne.walking = ARNE_SPEED
            self.player.talking = True

        self.new_bubble_timer += 1

        if self.player.rect.x - self.Arne.rect.x < TALKING_DISTANCE:
            self.Arne.walking = 0
            self.player.direction = "left"

            if self.bubble_count < len(self.speech_bubbles):
                if self.new_bubble_timer > 6:
                    key = py.key.get_pressed()
                    if (key[py.K_UP] or key[py.K_SPACE]) and self.pressed == False:
                        self.bubble_count += 1
                        self.new_bubble_timer = 0
                        self.pressed = True
                    if not (key[py.K_UP] or key[py.K_SPACE]):
                        self.pressed = False

            else:
                self.player.talking = False

        if self.player.rect.x < WIDTH - self.player.width // 2:
            if self.player.rect.colliderect(self.truck.rect):
                pass
                if self.lives == 1:
                    return Level4(self.lives, self.timer)
                else:
                    return Loose_screen()

        self.truck.update_sprite()
        self.truck.move()

        if self.player.rect.x > WIDTH:
            return Level5(self.lives, self.timer)

        if self.lives < 0:
            return Loose_screen()

    def draw(self):
        SCREEN.blit(bg_img_level4, (0, 0))
        self.player.draw()
        for car in self.cars:
            car.draw()
        self.truck.draw()
        self.Arne.draw()

        if self.player.talking and self.player.direction == "left" and self.bubble_count < len(self.speech_bubbles):
            draw_text("Trykk på mellomromstasten", font, WHITE, SCREEN, WIDTH // 2, HEIGHT // 6)
            self.speech_bubbles[self.bubble_count].draw()
        return super().draw()


class Level3(Level_scene):
    def __init__(self, lives, timer):
        super().__init__(world_data_3, START_POS, lives, timer)
        self.spike = Spike(-1 * TILE_SIZE, 12 * TILE_SIZE)
        self.homing_spike = False
        self.timer = timer

    def update(self):
        self.common_update()

        if self.player.vel_y < 0:
            self.homing_spike = True

        if self.player.rect.x > 700:
            self.homing_spike = True

        if self.homing_spike:
            if self.spike.hitbox[0] < self.player.rect.x:
                if self.player.rect.x - self.spike.hitbox[0] < 60:
                    self.spike.hitbox[0] += WALKING_SPEED
                    self.spike.x += WALKING_SPEED
                else:
                    self.spike.hitbox[0] += SPIKE_SPEED * 3
                    self.spike.x += SPIKE_SPEED * 3

        if self.player.rect.colliderect(self.spike.hitbox):
            pass
            if self.lives == 1:
                return Level3(self.lives, self.timer)
            else:
                return Loose_screen()

        if self.player.rect.x > WIDTH:
            return Level4(self.lives, self.timer)

        if self.lives < 0:
            return Loose_screen()

    def draw(self):
        SCREEN.blit(bg_img_level3, (0, 0))
        self.player.draw()
        self.spike.draw()
        return super().draw()


class Level2_5(Level_scene):
    def __init__(self, lives, timer):
        super().__init__(world_data_2_5, START_POS, lives, timer)
        self.spikes = []
        for i in range(1, 8):
            self.spikes.append(Spike(3 * i * TILE_SIZE, 8 * TILE_SIZE))
        self.timer = timer

    def update(self):
        self.common_update()

        for i in range(len(self.spikes)):
            if self.player.rect.colliderect(self.spikes[i].hitbox):
                pass
                if self.lives == 1:
                    return Level2_5(self.lives, self.timer)
                else:
                    return Loose_screen()

        if self.player.rect.y > HEIGHT:
            return Level4(self.lives, self.timer)

        if self.lives < 0:
            return Loose_screen()

    def draw(self):
        SCREEN.blit(bg_img_level2_5, (0, 0))
        self.player.draw()
        for i in range(len(self.spikes)):
            self.spikes[i].draw()
        return super().draw()


class Level2(Level_scene):
    def __init__(self, lives, timer):
        super().__init__(world_data_2, START_POS_2, lives, timer)
        self.portals = [Portal(280, 90), Portal(770, 90)]
        self.level_started = 0
        self.trap_activation = 5 * TILE_SIZE
        self.spikes = [Spike(8 * TILE_SIZE, 8 * TILE_SIZE), Spike(19 * TILE_SIZE, 9 * TILE_SIZE),
                       Spike(9 * TILE_SIZE, 4 * TILE_SIZE), Spike(10 * TILE_SIZE, 13 * TILE_SIZE)]
        for i in range(6):
            self.spikes.append(Spike((12 + i) * TILE_SIZE, 13 * TILE_SIZE))
        self.trap_timer = 0
        self.trap_activated = False
        self.timer = timer

    def update(self):
        self.common_update()
        for i in range(2):
            self.portals[i].update_sprite()

        # feller
        if self.player.rect.x > self.trap_activation - self.player.width * 1.8:
            self.level_started += 1

        if self.level_started == 1:
            self.spikes.insert(0, Spike(self.trap_activation, 11 * TILE_SIZE))
            self.trap_activated = True

        if self.trap_timer > 90:
            if self.trap_activated:
                self.trap_activated = False
                if len(self.spikes) > 10:
                    self.spikes.pop(3)
                self.trap_timer = 0
            else:
                self.trap_activated = True
                if len(self.spikes) < 11:
                    self.spikes.insert(3, Spike(9 * TILE_SIZE, 4 * TILE_SIZE))
                self.trap_timer = 0

        if self.player.rect.x > 21 * TILE_SIZE:
            if self.spikes[2].hitbox[0] < self.player.rect.x:
                self.spikes[2].hitbox[0] += SPIKE_SPEED
                self.spikes[2].x += SPIKE_SPEED

        for i in range(len(self.spikes)):
            if self.player.rect.colliderect(self.spikes[i].hitbox):
                pass
                if self.lives == 1:
                    return Level2(self.lives, self.timer)
                else:
                    return Loose_screen()

        # portalen
        if 280 < self.player.rect.x < 300 and 90 < self.player.rect.y < 200:  # definerer portalinngangen
            self.player.rect.x = 800

        if self.player.rect.x > WIDTH:
            return Level3(self.lives, self.timer)

        self.trap_timer += 1

        if self.lives < 0:
            return Loose_screen()

    def draw(self):
        SCREEN.blit(bg_img_level2, (0, 0))

        for i in range(2):
            self.portals[i].draw()

        self.player.draw()

        for i in range(len(self.spikes)):
            self.spikes[i].draw()

        return super().draw()


class Level1(Level_scene):
    def __init__(self, lives, timer):
        super().__init__(world_data_1, START_POS, lives, timer)
        self.hidden_tile_x = 17 * TILE_SIZE
        self.props = []
        self.spike = Spike(13 * TILE_SIZE, 12 * TILE_SIZE)
        self.timer = [0, 0, 0]
        for i in range(3):
            self.props.append(
                Prop(self.hidden_tile_x + TILE_SIZE * i, HEIGHT - TILE_SIZE, TILE_SIZE, TILE_SIZE, ground_img))

        self.speech_bubble = Speech_bubble(START_POS[0] * 0.5, HEIGHT // 4, "Didrik", ["Beveg deg med: A, D og", "mellomrom, eller piltaster"])

    def update(self):

        self.common_update()

        if self.player.rect.colliderect(self.spike.hitbox):
            pass
            if self.lives == 1:
                return Level1(self.lives, timer)
            else:
                return Loose_screen()

        if self.player.rect.y > HEIGHT:
            return Level2(self.lives, self.timer)
        if self.player.rect.x > WIDTH:
            return Level2_5(self.lives, self.timer)
        if self.lives < 0:
            return Loose_screen()

    def draw(self):
        SCREEN.blit(bg_img, (0, 0))

        draw_text("Du har 5 minutter på å rekke timen", font, WHITE, SCREEN, WIDTH // 2, HEIGHT // 6)

        if self.player.rect.x <= START_POS[0]:
            self.speech_bubble.draw()

        if self.player.rect.x < self.hidden_tile_x:
            for i in range(len(self.props)):
                self.props[i].draw()

        self.player.draw()
        self.spike.draw()
        return super().draw()


def draw_text(text, font, color, surface, x, y, timer = False):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if timer == True:
        textrect.topleft = (x, y)
    else:
        textrect.center = (x, y)

    surface.blit(textobj, textrect)
    return textrect




class Start_screen(Scene):
    last_chance_mode_img = pygame.image.load("assets/img/last_chance_mode.png").convert_alpha()
    normal_mode_img = pygame.image.load("assets/img/normal_mode.png").convert_alpha()
    last_chance_mode_hover_img = pygame.image.load("assets/img/last_chance_mode_hover.png").convert_alpha()
    normal_mode_hover_img = pygame.image.load("assets/img/normal_mode_hover.png").convert_alpha()

    # Justerer størrelsen på bildene
    last_chance_mode_img = pygame.transform.scale(last_chance_mode_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
    normal_mode_img = pygame.transform.scale(normal_mode_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
    last_chance_mode_hover_img = pygame.transform.scale(last_chance_mode_hover_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
    normal_mode_hover_img = pygame.transform.scale(normal_mode_hover_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

    # Posisjoner for knappene
    last_chance_mode_img_x = (WIDTH - BUTTON_WIDTH * 2 - BUTTON_SPACING) // 2
    normal_mode_img_x = last_chance_mode_img_x + BUTTON_WIDTH + BUTTON_SPACING

    def update(self):
        SCREEN.fill(START_COLOR)
        draw_text("Velg vanskelighetsgrad:", font, WHITE, SCREEN, WIDTH // 2, HEIGHT // 6)

        # Tegner standardbilder
        SCREEN.blit(self.normal_mode_img, (self.normal_mode_img_x, BUTTON_y))
        SCREEN.blit(self.last_chance_mode_img, (self.last_chance_mode_img_x, BUTTON_y))

        # Henter museposisjonen
        mouse_pos = pygame.mouse.get_pos()

        # Sjekker for hover-effekt og tegn hover-bilder
        if self.normal_mode_img.get_rect(topleft=(self.normal_mode_img_x, BUTTON_y)).collidepoint(mouse_pos):
            SCREEN.blit(self.normal_mode_hover_img, (self.normal_mode_img_x, BUTTON_y))
        if self.last_chance_mode_img.get_rect(topleft=(self.last_chance_mode_img_x, BUTTON_y)).collidepoint(mouse_pos):
            SCREEN.blit(self.last_chance_mode_hover_img, (self.last_chance_mode_img_x, BUTTON_y))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.last_chance_mode_img.get_rect(topleft=(self.last_chance_mode_img_x, BUTTON_y)).collidepoint(
                        mouse_pos):
                    # Start hovedspillet med 1 liv
                    return Level1(0, [0, 0, 0])

                elif self.normal_mode_img.get_rect(topleft=(self.normal_mode_img_x, BUTTON_y)).collidepoint(
                        mouse_pos):
                    # Start hovedspillet med 5 liv
                    return Level1(1, [0, 0, 0])


class Loose_screen(Scene):

    restart_img = pygame.image.load("assets/img/restart.png").convert_alpha()
    restart_hover_img = pygame.image.load("assets/img/restart_hover.png").convert_alpha()

    restart_img = pygame.transform.scale(restart_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
    restart_hover_img = pygame.transform.scale(restart_hover_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

    restart_img_x = (WIDTH / 2 - BUTTON_WIDTH / 2)


    def __init__(self):
        # SCREEN.fill(START_COLOR)
        self.bg_img = pygame.image.load("assets/backdrops/you_loose.png")
        self.restart_hover = False  # Legger til en tilstand for hover-effekten

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        # Sjekker om musen er over restart-knappen
        if self.restart_img.get_rect(topleft=(self.restart_img_x, BUTTON_y)).collidepoint(mouse_pos):
            self.restart_hover = True
        else:
            self.restart_hover = False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Sjekker om musen klikket på restart-knappen
                if self.restart_img.get_rect(topleft=(self.restart_img_x, BUTTON_y)).collidepoint(mouse_pos):
                    # Start hovedspillet med 1 liv
                    return Start_screen()

    def draw(self):
        SCREEN.blit(self.bg_img, (0, 0))
        draw_text("Du tapte!", font, WHITE, SCREEN, WIDTH // 2, HEIGHT // 6)
        draw_text("Du rakk ikke timen...", font, WHITE, SCREEN, WIDTH // 2, HEIGHT // 4)


        # Tegner restart-knappen basert på hover-tilstanden
        if self.restart_hover:
            SCREEN.blit(self.restart_hover_img, (self.restart_img_x, BUTTON_y + TILE_SIZE))
        else:
            SCREEN.blit(self.restart_img, (self.restart_img_x, BUTTON_y + TILE_SIZE))


async def main():
    game = Game(Start_screen())
    await game.run()
    pygame.quit()

asyncio.run(main())



