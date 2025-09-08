# STARTER
from pygame import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os
from pygame.locals import *
import random
from enum import Enum

#Image Prompt: Make me a 1:1 ratio image that is a background for the shop of a game that has these characters. The game is called Whack A' Brick. 

class GameState(Enum):
    MAIN_MENU = 0
    GAME_START = 1
    SHOP = 2

gameState = GameState.MAIN_MENU

class MoleState(Enum):
    ABSENT = 0
    CHARACTER_A = 1
    CHARACTER_B = 2
    CHARACTER_C = 3
    CHARACTER_D = 4
    CHARACTER_E = 5
    DEAD = 6

MolePossibleConfig = [MoleState.CHARACTER_A,MoleState.CHARACTER_B,MoleState.CHARACTER_C,MoleState.CHARACTER_D,MoleState.CHARACTER_E]

# need for making .exe later
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS #type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#PATHS
mole_absent_image_path = ".\\PNG\\Double\\Special\\extra_crate.png"
mole_paths = [".\\PNG\\Double\\Special\\extra_character_a.png",".\\PNG\\Double\\Special\\extra_character_b.png",".\\PNG\\Double\\Special\\extra_character_c.png",
                ".\\PNG\\Double\\Special\\extra_character_d.png",".\\PNG\\Double\\Special\\extra_character_e.png"]
background_path = "Whack_A_Brick_background.png"
braxton_image_path = "braxton-remove.png"
quit_button_image_path = "Quit_Button.png"
shop_background_image_path = "Shop.png"

# Sounds we want to use
pygame.mixer.init()
braxton_sound = pygame.mixer.Sound('among-us-roundstart.mp3')
moe_sound = pygame.mixer.Sound('cheese.mp3')

# set up the display
pygame.init()
screen = pygame.display.set_mode((700,700),pygame.NOFRAME)
pygame.display.set_caption("Whack A' Brick!")

#IMAGES
moleabsent = pygame.transform.scale(pygame.image.load(resource_path(mole_absent_image_path)).convert_alpha(),(90,90))
mole_alive = [(state,pygame.transform.scale(pygame.image.load(resource_path(mole_img)).convert_alpha(),(90,90))) for state,mole_img in zip(MolePossibleConfig,mole_paths)]
background_image = pygame.transform.scale(pygame.image.load(resource_path(background_path)).convert(),(700,700))
braxton_x = 612//4
braxton_y = 408//4
braxton_image = pygame.transform.scale(pygame.image.load(resource_path(braxton_image_path)).convert_alpha(),(braxton_x,braxton_y))
screen.blit(background_image, (0, 0))
screen.blit(braxton_image, (0, 700-408//4))
shop_background_image = pygame.transform.scale(pygame.image.load(resource_path(shop_background_image_path)).convert(),(700,700))

# Mole class
class Mole(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        orginal_x = 128
        orginal_y = 128
        ratio = 60/orginal_x
        after_x = int(orginal_x*ratio)
        after_y = int(orginal_y*ratio)
        self.image = pygame.transform.scale(pygame.image.load(resource_path(mole_absent_image_path)).convert_alpha(),(after_x,after_y))
        self.rect = self.image.get_rect().move(x+10,y-10)
        self.status = MoleState.ABSENT
        self.absent_image = pygame.transform.scale(pygame.image.load(resource_path(mole_absent_image_path)).convert_alpha(),(after_x,after_y))
        self.alive_image = pygame.transform.scale(pygame.image.load(resource_path(mole_absent_image_path)).convert_alpha(),(after_x,after_y))
        self.fading = False
        self.fade_alpha = 255
        self.original_image = None
    
    def update(self):
        if self.fading:
            self.fade_alpha -= 10  # Adjust this value to control fade speed (higher = faster fade)
            if self.fade_alpha <= 0:
                self.status = MoleState.ABSENT
                self.image = self.absent_image
                self.fading = False
            else:
                faded = self.original_image.copy()
                faded.set_alpha(self.fade_alpha)
                self.image = faded

# for timing
framerate = 1000  # you can modify to adjust speed of animation, 1 second = 1000 milliseconds
TIMEREVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEREVENT, framerate)

# Colors we want to use
pink = (255,157,195)
white = (255,255,255)
black = (0, 0, 0)
lightblue = (30,144,255)
darkblue = (0,0,139)
red = (255,0,0)

# create our moles
moles = [[None for _ in range(5)] for _ in range(5)]
x = 100
y = 100
for i in range(5):
    for j in range(5):
        moles[i][j] = Mole(x,y) #type: ignore
        x += 100
    x = 100
    y += 100

# create some fonts
headerfont = Font('freesansbold.ttf', 48)
buttonfont = pygame.font.SysFont('Corbel',32)
buttonfont.set_bold(True)

# create text and info for our quit button
quitButtonImage = pygame.transform.scale(pygame.image.load(resource_path(quit_button_image_path)).convert_alpha(),(73,32))
quitButtonRect = quitButtonImage.get_rect()
quitButtonx = 150
quitButtony = 600
quitButtonwidth = quitButtonRect.width
quitButtonheight = quitButtonRect.height
quitButtonRect.topleft = (quitButtonx,quitButtony)
pygame.draw.rect(screen,white,quitButtonRect)
screen.blit(quitButtonImage, quitButtonRect)

# create text and info for our shop button
shopButtonText = buttonfont.render(" Shop ", True, black, pink)
shopButtonRect = shopButtonText.get_rect()
shopButtonx = 300  # New position
shopButtony = 600
shopButtonwidth = shopButtonRect.width
shopButtonheight = shopButtonRect.height
shopButtonRect.topleft = (shopButtonx,shopButtony)
pygame.draw.rect(screen,white,shopButtonRect)
screen.blit(shopButtonText, shopButtonRect)

# # create text and info for our shop back button
shopBackButtonText = buttonfont.render(" Back ", True, black, pink)
shopBackButtonRect = shopBackButtonText.get_rect()
shopBackButtonx = 300  # New position
shopBackButtony = 600
shopBackButtonwidth = shopBackButtonRect.width
shopBackButtonheight = shopBackButtonRect.height
shopBackButtonRect.topleft = (shopBackButtonx,shopBackButtony)


# create text and info for our start button
startButtonText = buttonfont.render(" Start ", True, black, pink)
startButtonRect = startButtonText.get_rect()
print(startButtonRect)
startButtonx = 450
startButtony = 600
startButtonwidth = startButtonRect.width
startButtonheight = startButtonRect.height
startButtonRect.topleft = (startButtonx,startButtony)
pygame.draw.rect(screen,white,startButtonRect)
screen.blit(startButtonText, startButtonRect)

allmoles = Group(moles) #type: ignore
allmoles.draw(screen)

#Player Points
# Add this near the top where fonts are defined
pointsfont = pygame.font.SysFont('Corbel', 24)

initialGold = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == TIMEREVENT:
            # this means our timer went off!
            # randomly set moles to be up or down
            if gameState==GameState.GAME_START:
                for i in range(5):
                    for j in range(5):
                        # if mole was absent, randomly makeit alive
                        aliveodds = 20
                        absentodds = 3
                        if moles[i][j].status not in MolePossibleConfig:
                            r = random.randint(1,aliveodds)
                            if r == 1:
                                selected = random.choice(mole_alive)
                                moles[i][j].status = selected[0]
                                moles[i][j].image = selected[1]
                        # if alive, randomly make it absent
                        elif moles[i][j].status not in [MoleState.ABSENT,MoleState.DEAD]:
                            r = random.randint(1, absentodds)
                            if r == 1:
                                moles[i][j].status = MoleState.ABSENT
                                moles[i][j].image = moles[i][j].absent_image

        for i in range(5):
            for j in range(5):
                moles[i][j].update()
        # find mouse position
        mousePos = pygame.mouse.get_pos()
        mousex = mousePos[0]
        mousey = mousePos[1]
        if gameState==GameState.GAME_START:
            cursor_rect_pos = pygame.Rect(mousex,mousey,cursor_rect[2],cursor_rect[3])
        # print(mousex,mousey)

        if event.type == pygame.MOUSEBUTTONDOWN:
            # was the quit rectangle clicked?
            if mousex >= quitButtonx and mousex <= quitButtonx + quitButtonwidth and \
                mousey >= quitButtony and mousey <= quitButtony + quitButtonheight:
                pygame.quit()
                sys.exit()
            
            if gameState==GameState.MAIN_MENU and mousex >= startButtonx and mousex <= startButtonx + startButtonwidth and \
                mousey >= startButtony and mousey <= startButtony + startButtonheight:
                gameState = GameState.GAME_START
                playerPoints = 0
                pygame.mouse.set_visible(False)
                cursor_image = transform.scale(pygame.image.load("cursor.png"),(30,30))
                cursor_rect = cursor_image.get_rect()
            
            # Add shop button click
            if gameState==GameState.MAIN_MENU and mousex >= shopButtonx and mousex <= shopButtonx + shopButtonwidth and \
                mousey >= shopButtony and mousey <= shopButtony + shopButtonheight:
                gameState = GameState.SHOP
            
            # Add shop button click
            elif gameState==GameState.SHOP and mousex >= shopBackButtonx and mousex <= shopBackButtonx + shopBackButtonwidth and \
                mousey >= shopBackButtony and mousey <= shopBackButtony + shopBackButtonheight:
                gameState = GameState.MAIN_MENU
            
            #play amongus sound when braxton is clicked
            braxton_pos_x1 = 0
            braxton_pos_x2 = 0 + braxton_x
            braxton_pos_y1 = 700-408//4
            braxton_pos_y2 = 700

            if braxton_pos_x1<=mousex<=braxton_pos_x2 and braxton_pos_y1<=mousey<=braxton_pos_y2:
                braxton_sound.play()

            #play cheese when moe is clicked
            for a_moe in allmoles:
                if gameState==GameState.GAME_START:
                    if a_moe.status in MolePossibleConfig and a_moe.rect.colliderect(cursor_rect):
                        a_moe.status = MoleState.DEAD
                        a_moe.fading = True
                        a_moe.fade_alpha = 255
                        a_moe.original_image = a_moe.image.copy()
                        moe_sound.play()
                        playerPoints += 1


        
        
        # if hovering on a button, change its color
        # if mousex >= quitButtonx and mousex <= quitButtonx + quitButtonwidth and \
        #         mousey >= quitButtony and mousey <= quitButtony + quitButtonheight:
        #     quitButtonText = buttonfont.render(" Quit ", True, red, pink)
        # else:
        #     quitButtonText = buttonfont.render(" Quit ", True, black, pink)
        
        # draw the moles
        for a_mole in allmoles:
            if a_mole.status in MolePossibleConfig or a_mole.status == MoleState.DEAD:
                screen.blit(a_mole.image, a_mole.rect)
        #draw braxton
        screen.blit(braxton_image, (0, 700-408//4))

        if gameState==GameState.GAME_START:
            # paint the background
            screen.blit(background_image, (0, 0))

            cursor_rect.center = pygame.mouse.get_pos()
            #draw the cursor
            screen.blit(cursor_image, cursor_rect)
            pointsText = pointsfont.render(f"Points: {playerPoints}", True, black, pink)
            #draw the player point
            screen.blit(pointsText, (10, 10))

            if mousex >= quitButtonx and mousex <= quitButtonx + quitButtonwidth and \
                    mousey >= quitButtony and mousey <= quitButtony + quitButtonheight:
                quitButtonText = buttonfont.render(" Quit ", True, red, pink)
            else:
                quitButtonText = buttonfont.render(" Quit ", True, black, pink)       
        
            screen.blit(quitButtonText, quitButtonRect)

        elif gameState == GameState.SHOP:
            # paint the background
            screen.blit(shop_background_image, (0, 0))
            # Placeholder for shop: display text and back button
            shopText = headerfont.render("Shop Coming Soon!", True, black, pink)
            shopRect = shopText.get_rect()
            shopRect.center = (350, 300)
            screen.blit(shopText, shopRect)
            

            if mousex >= quitButtonx and mousex <= quitButtonx + quitButtonwidth and \
                    mousey >= quitButtony and mousey <= quitButtony + quitButtonheight:
                quitButtonText = buttonfont.render(" Quit ", True, red, pink)
            else:
                quitButtonText = buttonfont.render(" Quit ", True, black, pink)
            
            if mousex >= shopBackButtonx and mousex <= shopBackButtonx + shopBackButtonwidth and \
                    mousey >= shopBackButtony and mousey <= shopBackButtony + shopBackButtonheight:
                shopBackButtonText = buttonfont.render(" Back ", True, red, pink)
            else:
                shopBackButtonText = buttonfont.render(" Back ", True, black, pink)
        
            screen.blit(quitButtonText, quitButtonRect)
            pygame.draw.rect(screen,white,shopBackButtonRect)
            screen.blit(shopBackButtonText, shopBackButtonRect)

        elif gameState==GameState.MAIN_MENU:
            # paint the background
            screen.blit(background_image, (0, 0))
            if mousex >= quitButtonx and mousex <= quitButtonx + quitButtonwidth and \
                    mousey >= quitButtony and mousey <= quitButtony + quitButtonheight:
                quitButtonText = buttonfont.render(" Quit ", True, red, pink)
            else:
                quitButtonText = buttonfont.render(" Quit ", True, black, pink)
            
            if mousex >= shopButtonx and mousex <= shopButtonx + shopButtonwidth and \
                    mousey >= shopButtony and mousey <= shopButtony + shopButtonheight:
                shopButtonText = buttonfont.render(" Shop ", True, red, pink)
            else:
                shopButtonText = buttonfont.render(" Shop ", True, black, pink)
            
            if mousex >= startButtonx and mousex <= startButtonx + startButtonwidth and \
                    mousey >= startButtony and mousey <= startButtony + startButtonheight:
                startButtonText = buttonfont.render(" Start ", True, red, pink)
            else:
                startButtonText = buttonfont.render(" Start ", True, black, pink)
        
            screen.blit(quitButtonText, quitButtonRect)
            screen.blit(shopButtonText, shopButtonRect)
            screen.blit(startButtonText, startButtonRect)
        #update the display
        pygame.display.update()