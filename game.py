import pygame
import sys
from scripts.utils import load_image, load_images, load_sound, to_grid, to_pos, Animation, load_music, play_music, set_volume, queue_music
from scripts.constants import SCREEN_SIZE, DISPLAY_SIZE, WINDOW_TITLE, SPAWN_POS
from scripts.entities import Player
from scripts.bindings import Bindings
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.display = pygame.Surface(DISPLAY_SIZE, pygame.SRCALPHA)
        pygame.display.set_caption(WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.movement = [False, False]
        self.bindings = Bindings(self)
        self.assets = {
            'grapple-icon': load_image('grapple/grapple-icon.png'),
            'dirt': load_images('tiles/dirt'),
            'player/jump': Animation(load_images('player/jump'), img_dur=-1),
            'player/walk': Animation(load_images('player/walk'), img_dur=10),
            'player/idle': Animation(load_images('player/idle'), img_dur=12),
            'player/throwing': Animation(load_images('player/jump'), img_dur=-1),
            'player/grappling': Animation(load_images('player/jump'), img_dur=-1),
            'player/swinging': Animation(load_images('player/jump'), img_dur=-1),
            'grapple': load_image('grapple/grapple.png'),           
        }

        self.player = Player(self, to_pos(SPAWN_POS), (17, 32))

        self.sfx = {
            'jump': load_sound('jump.wav'),
            'throw': load_sound('throw.wav'),
            'grapple': load_sound('grapple.wav'),
        }

        self.sfx['jump'].set_volume(0.5)
        self.sfx['throw'].set_volume(.06)
        self.sfx['grapple'].set_volume(0.6)

        self.camera = [0, 0]

        self.tilemap = Tilemap(self)

    def run(self):
        
        load_music('grappling with it intro.wav')
        set_volume(0.5)
        play_music()
        queue_music('grappling with it loop.wav', loops=-1)

        while True:
            self.display.fill((0, 0, 0))

            self.camera[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.camera[0]) / 30
            self.camera[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.camera[1]) / 30

            self.tilemap.render(self.display, offset=self.camera)
            
            frame_movement = ((self.movement[1] - self.movement[0]) * self.player.walk_speed, 0)

            self.player.update(self.tilemap, frame_movement)
            self.player.render(self.display, offset=self.camera)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                self.bindings.read_input(self, event)
                            
            self.screen.blit(pygame.transform.scale(self.display, SCREEN_SIZE), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

            #print(to_grid(self.player.pos))
            #print(self.player.action)
            
Game().run()