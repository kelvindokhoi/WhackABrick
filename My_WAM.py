# STARTER
from pygame import * #type:ignore
from pygame.font import Font
from pygame.sprite import * #type:ignore
import pygame, sys
from pygame.locals import * #type:ignore
import random
from enum import Enum
from peewee import * #type:ignore
from tkinter import messagebox

#functions
from functions.Buffs import BUFF
from functions.Database import Database
from functions.Resource_Reader import resource_path,image_loader
from functions.FilePaths import * #type:ignore
from functions.Colors import * #type:ignore
from functions.Bricks import brickState,Brick,BrickObject
from functions.GameState import GameState
from functions.Music import Music
from functions.CalculateScore import caclculate_score
from functions.Braxton import BraxtonObject
from functions.Button import Button
from functions.All_Buttons import * #type:ignore
from functions.Fonts import GameFonts
from functions.DisplaySettings import initialize_display

# Game modes (developer options)
debug_mode = False
connect_to_database = False

# Displays
screen,desktop_width,desktop_height = initialize_display()
background_image = image_loader(background_169_path,(desktop_width,desktop_height),False)
shop_background_image = image_loader(shop_background_image_path,(desktop_width,desktop_height),False)

# Initializing objects
MyDB = Database(connect_to_database)
gameState = GameState.MAIN_MENU
music = Music()
braxtonObject = BraxtonObject(desktop_height)
gameFont = GameFonts()
brickObject = BrickObject()
quitButtonObject = QuitButtonObject()
shopButtonObject = ShopButtonObject()
shopBackButtonObject = ShopBackButtonObject()
startButtonObject = StartButtonObject()
startBackButtonObject = StartBackButtonObject()
settingsButtonObject = SettingsButtonObject(desktop_width)

# Timing
framerate = 1000  # you can modify to adjust speed of animation, 1 second = 1000 milliseconds
TIMEREVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEREVENT, framerate)

# Parameters
initialGold = 0
buffs = [BUFF.AUTOCLICK,BUFF.X2SCOREMULTIPLIER,BUFF.X3SCOREMULTIPLIER]

# Cursor settings
pygame.mouse.set_visible(False)
cursor_image = transform.scale(pygame.image.load(resource_path(cursor_image_path)),(30,30))
cursor_Rect = cursor_image.get_rect()
cursor_Rect.center = pygame.mouse.get_pos()

while True:
    cursor_Rect = cursor_image.get_rect()
    cursor_Rect.center = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == TIMEREVENT:brickObject.random_brick(gameState)
        brickObject.update_brick()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # was the quit rectangle clicked?
            quitButtonObject.if_clicked(cursor_Rect)
            
            match gameState:
                case GameState.MAIN_MENU:
                    # When the GAME_START, change the cursor image
                    if startButtonObject.rect.colliderect(cursor_Rect):
                        gameState = GameState.GAME_START
                        playerPoints = 0
                    # When shop button is clicked, change to SHOP
                    elif shopButtonObject.rect.colliderect(cursor_Rect):
                        gameState = GameState.SHOP
                    braxtonObject.if_collide_braxton(cursor_Rect,music)
                # When shop's back button is clicked, changes to MAIN_MENU
                case GameState.SHOP:
                    if shopBackButtonObject.rect.colliderect(cursor_Rect):
                        gameState = GameState.MAIN_MENU
                case GameState.GAME_START:
                    if startBackButtonObject.rect.colliderect(cursor_Rect):
                        gameState = GameState.MAIN_MENU
                    playerPoints = brickObject.if_brick_collide(cursor_Rect,playerPoints,buffs,music)
                    braxtonObject.if_collide_braxton(cursor_Rect,music)

    match gameState:
        case GameState.GAME_START:
            # paint the background and cursor
            screen.blit(background_image, (0, 0))
            
            #player point
            gameFont.blit_player_point(playerPoints,screen)

            quitButtonObject.if_hover(cursor_Rect)
            startBackButtonObject.if_hover(cursor_Rect)
            settingsButtonObject.if_hover(cursor_Rect)

            quitButtonObject.blit_button(screen)
            startBackButtonObject.blit_button(screen)
            settingsButtonObject.blit_button(screen)

            if BUFF.AUTOCLICK in buffs:
                playerPoints = brickObject.if_brick_collide(cursor_Rect,playerPoints,buffs,music)

            brickObject.blit_brick(screen)
            braxtonObject.blit_braxton(screen)

        case GameState.SHOP:
            # paint the background
            screen.blit(shop_background_image, (0, 0))
            # Placeholder for shop: display text and back button
            gameFont.blit_shop_text(screen)

            quitButtonObject.if_hover(cursor_Rect)
            shopBackButtonObject.if_hover(cursor_Rect)
            settingsButtonObject.if_hover(cursor_Rect)
        
            quitButtonObject.blit_button(screen)
            shopBackButtonObject.blit_button(screen)
            settingsButtonObject.blit_button(screen)

        case GameState.MAIN_MENU:
            # paint the background
            screen.blit(background_image, (0, 0))

            quitButtonObject.if_hover(cursor_Rect)
            shopButtonObject.if_hover(cursor_Rect)
            startButtonObject.if_hover(cursor_Rect)
            settingsButtonObject.if_hover(cursor_Rect)

            braxtonObject.blit_braxton(screen)
            quitButtonObject.blit_button(screen)
            shopButtonObject.blit_button(screen)
            startButtonObject.blit_button(screen)
            settingsButtonObject.blit_button(screen)

        case default:
            pass
    # pygame.draw.rect(screen, (0,255,0), startButtonRect, 2)  # green outline
    quitButtonObject.debug_mode(screen,debug_mode)
    shopButtonObject.debug_mode(screen,debug_mode)
    brickObject.debug_mode_brick(screen,debug_mode)
    settingsButtonObject.debug_mode(screen,debug_mode)
    #update the display
    screen.blit(cursor_image, cursor_Rect)
    pygame.display.update()