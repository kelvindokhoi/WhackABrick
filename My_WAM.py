# STARTER
from pygame import * #type:ignore
from pygame.font import Font
from pygame.sprite import * #type:ignore
import pygame, sys
from pygame.locals import * #type:ignore
import random
from enum import Enum
from peewee import * #type:ignore

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

connect_to_database = False
MyDB = Database(connect_to_database)

gameState = GameState.MAIN_MENU

# Sounds we want to use
music = Music()

#Initialize display
if pygame.get_init()==False:
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN,pygame.NOFRAME)
    infoObject = pygame.display.Info()
    desktop_width = infoObject.current_w
    desktop_height = infoObject.current_h
    pygame.display.set_caption("Whack A' Brick!")
else:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN,pygame.NOFRAME)
    infoObject = pygame.display.Info()
    desktop_width = infoObject.current_w
    desktop_height = infoObject.current_h


background_image = image_loader(background_169_path,(desktop_width,desktop_height),False)
shop_background_image = image_loader(shop_background_image_path,(desktop_width,desktop_height),False)
settings_image = pygame.image.load(resource_path(settings_image_path)).convert_alpha()

braxtonObject = BraxtonObject(desktop_height)

# for timing
framerate = 1000  # you can modify to adjust speed of animation, 1 second = 1000 milliseconds
TIMEREVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEREVENT, framerate)

brickObject = BrickObject()

# create some fonts
if True:
    headerfont = Font('freesansbold.ttf', 48)
    buttonfont = pygame.font.SysFont('Corbel',32)
    buttonfont.set_bold(True)

# create text and info for our quit button

quitButtonImage = pygame.transform.scale(pygame.image.load(resource_path(quit_button_image_path)).convert_alpha(),(150+15,62+10))
quitButtonImageHover = pygame.transform.scale(pygame.image.load(resource_path(quit_button_hover_image_path)).convert_alpha(),(150+10,62+5))
quitButtonCurrentImage = quitButtonImage
quitButtonRect = quitButtonImage.get_rect()
quitButtonRect.topleft = (500,850)
screen.blit(quitButtonCurrentImage, quitButtonRect)


# create text and info for our shop button
shopButtonImage = pygame.transform.scale(pygame.image.load(resource_path(shop_button_image_path)).convert_alpha(),(150+10,62+5))
shopButtonImageHover = pygame.transform.scale(pygame.image.load(resource_path(shop_button_hover_image_path)).convert_alpha(),(150,62))
shopButtonCurrentImage = shopButtonImage
shopButtonRect = shopButtonImage.get_rect()
shopButtonRect.topleft = (950,850)
screen.blit(shopButtonCurrentImage, shopButtonRect)

# # create text and info for our shop back button
shopBackButtonImage = pygame.transform.scale(pygame.image.load(resource_path(shop_back_button_image_path)).convert_alpha(),(150+10,62+5))
shopBackButtonImageHover = pygame.transform.scale(pygame.image.load(resource_path(shop_back_button_hover_image_path)).convert_alpha(),(150,62))
shopBackButtonCurrentImage = shopBackButtonImage
shopBackButtonRect = shopBackButtonImage.get_rect()
shopBackButtonRect.topleft = (950,850)
screen.blit(shopBackButtonCurrentImage, shopBackButtonRect)


# create button for START_GAME
startButtonImage = pygame.transform.scale(pygame.image.load(resource_path(start_button_image_path)).convert_alpha(),(150+10,62+5))
startButtonImageHover = pygame.transform.scale(pygame.image.load(resource_path(start_button_hover_image_path)).convert_alpha(),(150,62))
startButtonCurrentImage = startButtonImage
startButtonRect = startButtonImage.get_rect()
startButtonRect.topleft = (1400,850)
screen.blit(startButtonImage, startButtonRect)

# create back button for START_GAME
startBackButtonImage = pygame.transform.scale(pygame.image.load(resource_path(shop_back_button_image_path)).convert_alpha(),(150+10,62+5))
startBackButtonImageHover = pygame.transform.scale(pygame.image.load(resource_path(shop_back_button_hover_image_path)).convert_alpha(),(150,62))
startBackButtonCurrentImage = startBackButtonImage
startBackButtonRect = startBackButtonImage.get_rect()
startBackButtonRect.topleft = (1400,850)
screen.blit(startBackButtonCurrentImage, startBackButtonRect)

#create settings button
settingsButtonwidth = settingsButtonheight = 100
settingsButton = pygame.transform.scale(settings_image.convert_alpha(),(100,100))
settingsButtonx = desktop_width-100
settingsButtony = 0
settingsButtonRect = settingsButton.get_rect()
settingsButtonRect.topleft = (settingsButtonx,settingsButtony)
screen.blit(settingsButton,settingsButtonRect)
pygame.draw.rect(screen, blue, shopButtonRect, 2)


#Player Points
# Add this near the top where fonts are defined
pointsfont = pygame.font.SysFont('Corbel', 69)
pointsfont.set_bold(True)

# parameters
initialGold = 0

pygame.mouse.set_visible(False)
cursor_image = transform.scale(pygame.image.load(resource_path(cursor_image_path)),(30,30))
cursor_Rect = cursor_image.get_rect()
cursor_Rect.center = pygame.mouse.get_pos()

#buffs
buffs = []


while True:
    cursor_Rect = cursor_image.get_rect()
    cursor_Rect.center = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == TIMEREVENT:
            # this means our timer went off!
            # randomly set bricks to be up or down
            brickObject.random_brick(gameState)

        brickObject.update_brick()


        if event.type == pygame.MOUSEBUTTONDOWN:
            # was the quit rectangle clicked?
            if quitButtonRect.colliderect(cursor_Rect):
                pygame.quit()
                sys.exit()
            
            match gameState:
                case GameState.MAIN_MENU:
                    # When the GAME_START, change the cursor image
                    if startButtonRect.colliderect(cursor_Rect):
                        gameState = GameState.GAME_START
                        playerPoints = 0
                    # When shop button is clicked, change to SHOP
                    elif shopButtonRect.colliderect(cursor_Rect):
                        gameState = GameState.SHOP
                    braxtonObject.if_collide_braxton(cursor_Rect,music)
                # When shop's back button is clicked, changes to MAIN_MENU
                case GameState.SHOP:
                    if shopBackButtonRect.colliderect(cursor_Rect):
                        gameState = GameState.MAIN_MENU
                case GameState.GAME_START:
                    if startBackButtonRect.colliderect(cursor_Rect):
                        gameState = GameState.MAIN_MENU
                    #when moe is clicked, make it fade, play sound, increase pointsfor i in range(5):
                    playerPoints = brickObject.if_brick_collide(cursor_Rect,playerPoints,buffs,music)
                    braxtonObject.if_collide_braxton(cursor_Rect,music)

    match gameState:
        case GameState.GAME_START:
            # paint the background and cursor
            screen.blit(background_image, (0, 0))
            
            #player point
            pointsText = pointsfont.render(f"Points: {playerPoints}", True, darkblue)
            screen.blit(pointsText, (90, 10))

            if quitButtonRect.colliderect(cursor_Rect):
                quitButtonCurrentImage = quitButtonImageHover
            else:
                quitButtonCurrentImage = quitButtonImage

            if startBackButtonRect.colliderect(cursor_Rect):
                startBackButtonCurrentImage = startBackButtonImageHover
            else:
                startBackButtonCurrentImage = startBackButtonImage

            screen.blit(startBackButtonCurrentImage, startButtonRect)
            screen.blit(quitButtonCurrentImage, quitButtonRect)
            screen.blit(settingsButton,settingsButtonRect)
            pygame.draw.rect(screen, blue, settingsButtonRect, 5)

            if BUFF.AUTOCLICK in buffs:
                playerPoints = brickObject.if_brick_collide(cursor_Rect,playerPoints,buffs,music)

            brickObject.blit_brick(screen)
            braxtonObject.blit_braxton(screen)

        case GameState.SHOP:
            # paint the background
            screen.blit(shop_background_image, (0, 0))
            # Placeholder for shop: display text and back button
            shopText = headerfont.render("Shop Coming Soon!", True, black, pink)
            shopRect = shopText.get_rect()
            shopRect.center = (350, 300)
            screen.blit(shopText, shopRect)
            

            if quitButtonRect.colliderect(cursor_Rect):
                quitButtonCurrentImage = quitButtonImageHover
            else:
                quitButtonCurrentImage = quitButtonImage
            
            if shopBackButtonRect.colliderect(cursor_Rect):
                shopBackButtonCurrentImage = shopBackButtonImageHover
            else:
                shopBackButtonCurrentImage = shopBackButtonImage
        
            screen.blit(quitButtonCurrentImage, quitButtonRect)
            screen.blit(shopBackButtonCurrentImage, shopBackButtonRect)
            screen.blit(settingsButton,settingsButtonRect)
            pygame.draw.rect(screen, blue, settingsButtonRect, 5)

        case GameState.MAIN_MENU:
            # paint the background
            screen.blit(background_image, (0, 0))

            if quitButtonRect.colliderect(cursor_Rect):
                quitButtonCurrentImage = quitButtonImageHover
            else:
                quitButtonCurrentImage = quitButtonImage
            
            if shopButtonRect.colliderect(cursor_Rect):
                shopButtonCurrentImage = shopButtonImageHover
            else:
                shopButtonCurrentImage = shopButtonImage
            
            if startButtonRect.colliderect(cursor_Rect):
                startButtonCurrentImage = startButtonImageHover
            else:
                startButtonCurrentImage = startButtonImage

            braxtonObject.blit_braxton(screen)
            screen.blit(quitButtonCurrentImage, quitButtonRect)
            screen.blit(shopButtonCurrentImage, shopButtonRect)
            screen.blit(startButtonCurrentImage, startButtonRect)
            screen.blit(settingsButton,settingsButtonRect)
            pygame.draw.rect(screen, blue, settingsButtonRect, 5)

        # pygame.draw.rect(screen, (0,255,0), startButtonRect, 2)  # green outline
        # pygame.draw.rect(screen, (255,0,0), quitButtonRect, 2)   # red outline
        # pygame.draw.rect(screen, (0,0,255), shopButtonRect, 2)   # blue outline
    brickObject.debug_mode_brick(screen)
    #update the display
    screen.blit(cursor_image, cursor_Rect)
    pygame.display.update()