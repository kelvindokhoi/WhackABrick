# from pygame.locals import * #type:ignore
# from pygame import *
import pygame
from functions.FilePaths import amongus_sound_path,cheese_sound_path,background_music_path
from functions.Resource_Reader import resource_path

class Music:
    def __init__(self):
        pygame.mixer.init()
        self.braxton_sound = pygame.mixer.Sound(resource_path(amongus_sound_path))
        self.brick_hit_sound = pygame.mixer.Sound(resource_path(cheese_sound_path))
        self.background_music = pygame.mixer.music.load(resource_path(background_music_path))
        pygame.mixer.music.play(-1)
    
    def play_brick_hit_sound(self):
        self.brick_hit_sound.play()