# STARTER
from pygame import * #type:ignore
from pygame.font import Font
from pygame.sprite import * #type:ignore
import pygame, sys
from pygame.locals import * #type:ignore
import random
from enum import Enum
from peewee import * #type:ignore
import tkinter as tk
from tkinter import messagebox
import math

#functions
from functions.Buffs import BUFF
from functions.Database import Database
from functions.Resource_Reader import resource_path,image_loader
from functions.FilePaths import * #type:ignore
from functions.Colors import * #type:ignore
from functions.Bricks import brickState,Brick,BrickObject,Explosion
from functions.GameState import GameState
from functions.Music import Music
from functions.CalculateScore import caclculate_score
from functions.Braxton import BraxtonObject
from functions.Button import Button
from functions.All_Buttons import * #type:ignore
from functions.Fonts import GameFonts
from functions.DisplaySettings import initialize_display
from functions.Leaderboard import LeaderboardObject,CustomDialog,CustomDialogNL
from functions.Settings import SettingsObject
from functions.Shop import ShopObject
from functions.FilePaths import enhanced_cursor_image_path

# Game modes (developer options)
debug_mode = False
connect_to_database = True

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
leaderboardButtonObject = LeaderboardButtonObject()
leaderboardObject = LeaderboardObject(desktop_width,desktop_height)
settingsObject = SettingsObject(desktop_width, desktop_height)
shopObject = ShopObject()

# Timing
framerate = 1000  # you can modify to adjust speed of animation, 1 second = 1000 milliseconds
TIMEREVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEREVENT, framerate)

# Parameters
initialGold = 0
buffs = []
COUNTDOWN = 61
playerGold = 0
playerPoints = 0
countdown = COUNTDOWN

# Cursor settings
pygame.mouse.set_visible(False)
normal_cursor_image = transform.scale(pygame.image.load(resource_path(cursor_image_path)),(30,30))
cursor_Rect = normal_cursor_image.get_rect()
cursor_Rect.center = pygame.mouse.get_pos()
current_background_image = background_image
settings_visible = False
autoclick_cursor_image = image_loader(enhanced_cursor_image_path,(50,50))
current_cursor_image = normal_cursor_image

previous_game_state = gameState

while True:
    if BUFF.AUTOCLICK in buffs:
        current_cursor_image = autoclick_cursor_image
    else:
        cursor_Rect = current_cursor_image.get_rect()
    cursor_Rect.center = pygame.mouse.get_pos()

    events = pygame.event.get()
    for singular_event in events:
        if singular_event.type == QUIT:
            pygame.quit()
            sys.exit()

        if singular_event.type == TIMEREVENT and not settings_visible and gameState==GameState.GAME_START:
            brickObject.random_brick(gameState)
            if gameState == GameState.GAME_START:
                countdown -= 1

        if settings_visible and gameState == GameState.SETTINGS:
            if singular_event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
                settingsObject.handle_event(singular_event, cursor_Rect, music, playerGold, buffs)

        if singular_event.type == pygame.MOUSEBUTTONDOWN:
            # was the quit rectangle clicked?
            quitButtonObject.if_clicked(cursor_Rect)

            if settingsButtonObject.rect.colliderect(cursor_Rect):
                settings_visible = True
                old_gameState = gameState
                gameState = GameState.SETTINGS

            if gameState == GameState.SETTINGS:
                close_flag, new_gold = settingsObject.handle_event(singular_event, cursor_Rect, music, playerGold, buffs)
                if close_flag:
                    settings_visible = False
                    gameState = old_gameState
                    if new_gold is not None:
                        playerGold = new_gold
                    
            match gameState:
                case GameState.MAIN_MENU:
                    # When the GAME_START, change the cursor image
                    if startButtonObject.rect.colliderect(cursor_Rect):
                        gameState = GameState.GAME_START
                        playerPoints = 0
                        countdown = COUNTDOWN
                    # When shop button is clicked, change to SHOP
                    elif shopButtonObject.rect.colliderect(cursor_Rect):
                        gameState = GameState.SHOP
                        current_background_image = shop_background_image
                    elif leaderboardButtonObject.rect.colliderect(cursor_Rect):
                        scores,scoreVals = MyDB.read_top_3()
                        gameState = GameState.LEADERBOARD
                    braxtonObject.if_collide_braxton(cursor_Rect,music)
                # When shop's back button is clicked, changes to MAIN_MENU

                case GameState.SHOP:
                    if shopBackButtonObject.rect.colliderect(cursor_Rect):
                        gameState = GameState.MAIN_MENU
                        current_background_image = background_image

                        # reset shop feedback immediately
                        shopObject.feedback_text = None
                        shopObject.feedback_timer = 0

                    elif leaderboardButtonObject.rect.colliderect(cursor_Rect):
                        scores,scoreVals = MyDB.read_top_3()
                        gameState = GameState.LEADERBOARD
                    else:
                        playerGold, buffs = shopObject.if_clicked(events, buffs, playerGold, music)

                case GameState.GAME_START:
                    if startBackButtonObject.rect.colliderect(cursor_Rect):
                        gameState = GameState.MAIN_MENU
                        brickObject.__init__()
                    else:
                        if BUFF.BRICK17 in buffs:
                            killed_any = False
                            for brick in brickObject.allbricks:
                                if brick.status in brickObject.brickPossibleConfig:
                                    killed_any = True
                                    brick.status = brickState.DEAD
                                    brick.fading = True
                                    brick.fade_alpha = 255
                                    brick.original_image = brick.image.copy()
                                    playerPoints = caclculate_score(playerPoints, buffs)
                                    exp_pos = brick.rect.center
                                    brickObject.explosions.append(Explosion(exp_pos))
                            if killed_any:
                                music.play_brick_hit_sound()
                        else:
                            playerPoints = brickObject.if_brick_collide(cursor_Rect,playerPoints,buffs,music)
                    braxtonObject.if_collide_braxton(cursor_Rect,music)

                case GameState.LEADERBOARD:
                    if shopBackButtonObject.rect.colliderect(cursor_Rect):
                        gameState = GameState.MAIN_MENU

    if gameState != previous_game_state:
        music.switch_theme(gameState)
        previous_game_state = gameState

    music.update()

    brickObject.update_brick()

    screen.blit(current_background_image,(0,0))
    match gameState:
        case GameState.GAME_START:
            
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

            gameFont.blit_timer(screen,countdown)

            if countdown==0:
                earnedGold = int(math.sqrt(playerPoints)) + 2*buffs.count(BUFF.GOLDBUFF)
                playerGold += earnedGold
                scores,scoreVals = MyDB.read_top_3()
                if playerPoints>min(scoreVals):
                    gameState = GameState.SCORE_INPUT
                    leaderboardObject.ask_name(MyDB,playerPoints,earnedGold)
                    playerPoints = 0
                    gameState = GameState.MAIN_MENU
                else:
                    leaderboardObject.show_player_score(playerPoints,MyDB,earnedGold)
                    gameState = GameState.MAIN_MENU

        case GameState.SHOP:
            # Placeholder for shop: display text and back button
            gameFont.blit_shop_text(screen)

            quitButtonObject.if_hover(cursor_Rect)
            shopBackButtonObject.if_hover(cursor_Rect)
            settingsButtonObject.if_hover(cursor_Rect)
            leaderboardButtonObject.if_hover(cursor_Rect)
        
            quitButtonObject.blit_button(screen)
            shopBackButtonObject.blit_button(screen)
            settingsButtonObject.blit_button(screen)
            leaderboardButtonObject.blit_button(screen)

            shopObject.blit_shop_items(screen,buffs,playerGold,cursor_Rect)
            # pygame.draw.rect(screen,(0,0,225),shopObject.mult_exp_rect,2) #debug
            if cursor_Rect.colliderect(shopObject.mult_exp_rect):
                screen.blit(shopObject.multiplier_explanation_text,shopObject.score_multiplier_explanation_position)

        case GameState.MAIN_MENU:

            quitButtonObject.if_hover(cursor_Rect)
            shopButtonObject.if_hover(cursor_Rect)
            startButtonObject.if_hover(cursor_Rect)
            settingsButtonObject.if_hover(cursor_Rect)
            leaderboardButtonObject.if_hover(cursor_Rect)

            braxtonObject.blit_braxton(screen)
            quitButtonObject.blit_button(screen)
            shopButtonObject.blit_button(screen)
            startButtonObject.blit_button(screen)
            settingsButtonObject.blit_button(screen)
            leaderboardButtonObject.blit_button(screen)

        case GameState.LEADERBOARD:
            
            leaderboardObject.blit_leaderboard(screen,scores,gameFont)

            shopBackButtonObject.if_hover(cursor_Rect)

            shopBackButtonObject.blit_button(screen)

        case GameState.SETTINGS:
            settingsObject.draw(screen)

        case default:
            pass
 

    quitButtonObject.debug_mode(screen,debug_mode)
    shopButtonObject.debug_mode(screen,debug_mode)
    brickObject.debug_mode_brick(screen,debug_mode)
    settingsButtonObject.debug_mode(screen,debug_mode)
    #update the display
    screen.blit(current_cursor_image, cursor_Rect)
    pygame.display.update()