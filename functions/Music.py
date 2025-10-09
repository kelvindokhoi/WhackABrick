# from pygame.locals import * #type:ignore
# from pygame import *
import pygame
from functions.FilePaths import amongus_sound_path,cheese_sound_path,background_music_path,ding_sound,pop_sound,ttbling_sound,get_coin_sound,game_start_theme_path,leaderboard_theme_path,settings_theme,shop_theme,main_theme
from functions.Resource_Reader import resource_path
import random
from functions.GameState import GameState

class Music:
    def __init__(self):
        pygame.mixer.init()
        self.braxton_sound = pygame.mixer.Sound(resource_path(amongus_sound_path))
        self.cheese_sound = pygame.mixer.Sound(resource_path(cheese_sound_path))
        self.ttbling_sound = pygame.mixer.Sound(resource_path(ttbling_sound))
        self.ding_sound = pygame.mixer.Sound(resource_path(ding_sound))
        self.pop_sound = pygame.mixer.Sound(resource_path(pop_sound))
        self.get_coin_sound = pygame.mixer.Sound(resource_path(get_coin_sound))
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        self.update_sfx_volumes()
        self.saved_positions = {}
        self.current_state = GameState.MAIN_MENU
        self.pending_switch = None
        self.theme_paths = {
            GameState.MAIN_MENU: main_theme,
            GameState.SHOP: shop_theme,
            GameState.GAME_START: game_start_theme_path,
            GameState.LEADERBOARD: leaderboard_theme_path,
            GameState.SETTINGS: settings_theme,
        }
        pygame.mixer.music.set_volume(self.music_volume)
        # Play main theme immediately
        pygame.mixer.music.load(resource_path(main_theme))
        pygame.mixer.music.play(loops=-1)
    
    def update_sfx_volumes(self):
        for sound in [self.braxton_sound, self.cheese_sound, self.ttbling_sound, self.ding_sound, self.pop_sound, self.get_coin_sound]:
            sound.set_volume(self.sfx_volume)
    
    def switch_theme(self, new_state):
        if new_state == self.current_state:
            return
        # Save position of current
        if pygame.mixer.music.get_busy():
            self.saved_positions[self.current_state] = pygame.mixer.music.get_pos()
        self.current_state = new_state
        start_pos = self.saved_positions.get(new_state, 0) / 1000.0
        pygame.mixer.music.fadeout(1000)
        # Set pending switch
        self.pending_switch = (new_state, start_pos)
    
    def update(self):
        if self.pending_switch and not pygame.mixer.music.get_busy():
            state, start_pos = self.pending_switch
            path = self.theme_paths[state]
            pygame.mixer.music.load(resource_path(path))
            pygame.mixer.music.play(loops=-1, fade_ms=1000, start=start_pos)
            pygame.mixer.music.set_volume(self.music_volume)
            self.pending_switch = None
    
    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)
    
    def set_sfx_volume(self, volume):
        self.sfx_volume = volume
        self.update_sfx_volumes()
    
    def play_brick_hit_sound(self):
        if random.random() < 0.05:
            self.cheese_sound.play()
        else:
            sounds = [self.ttbling_sound, self.ding_sound, self.pop_sound]
            random.choice(sounds).play()
    
    def play_get_coin_sound(self):
        self.get_coin_sound.play()
    
    def play_braxton_sound(self):
        self.braxton_sound.play()