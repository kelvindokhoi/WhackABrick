# STARTER
from pygame import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os
from pygame.locals import *
import random
from enum import Enum
from peewee import *

connect_to_database = False
if connect_to_database == True:
    #Image Prompt: Make me a 1:1 ratio image that is a background for the shop of a game that has these characters. The game is called Whack A' Brick. 

    #DATABASE TESTING
    #1. Define the database connection
    # Replace with your actual MySQL credentials
    db = MySQLDatabase(
        'whackabrick',
        host='localhost',
        port=3306,
        user='root',
        password='root'
    )

    #2. Define a base model for your database
    class BaseModel(Model):
        class Meta:
            database = db

    #3. Define your model(s) that map to your database tables
    class Scores(BaseModel):
        #ScoreID = AutoField() # Peewee automatically handles primary keys
        ScoreName = CharField()
        ScoreVal = IntegerField()

    #4. Connect to the database
    db.connect()

    #5. Read data from the database
    #Select high scores
    scores = [None for _ in range(3)]
    scoreVals = [None for _ in range(3)]

    db_cursor = db.execute_sql("select scores.scorename, scores.scoreval from scores order by scores.scoreval desc limit 3")

    i=0
    for row in db_cursor.fetchall():
        #print(row[0],row[1])
        scores[i] = row[0] + "  " + str(row[1])  
        scoreVals[i] = row[1]
        print(scores[i])
        i+=1

    db.close()
    # for i in range(3):
    #     print(scores[i],scoreVals[i])

class GameState(Enum):
    MAIN_MENU = 0
    GAME_START = 1
    SHOP = 2
    SETTINGS = 3


gameState = GameState.MAIN_MENU

class brickState(Enum):
    ABSENT = 0
    CHARACTER_A = 1
    CHARACTER_B = 2
    CHARACTER_C = 3
    CHARACTER_D = 4
    CHARACTER_E = 5
    DEAD = 6

brickPossibleConfig = [brickState.CHARACTER_A,brickState.CHARACTER_B,brickState.CHARACTER_C,brickState.CHARACTER_D,brickState.CHARACTER_E]

class BUFF(Enum):
    AUTOCLICK = 0
    INCREASEINITIALGOLD = 1
    WRONGCLICKSHIELD = 2
    X2SCOREMULTIPLIER = 3
    X3SCOREMULTIPLIER = 4
    X4SCOREMULTIPLIER = 5
    X5SCOREMULTIPLIER = 6
    X6SCOREMULTIPLIER = 7
    X7SCOREMULTIPLIER = 8
    X8SCOREMULTIPLIER = 9
    X9SCOREMULTIPLIER = 10
    X10SCOREMULTIPLIER = 11
    INCREASEHITBOX = 12
    SHOPPROMOTION = 13
    LUCKY = 14
    EXTRADAMAGE = 15
    MASSEXTINCTIONCLICK = 16
    INCREASEPASSIVEGOLD = 17
    INCREASELOOT =18
    TIMESLOWDOWN = 19
    PERIODICTHORTUHNDER = 20



def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores files in sys._MEIPASS/resource
        base_path = os.path.join(sys._MEIPASS, "resource")
    except AttributeError:
        # In development, use the resource directory
        base_path = os.path.abspath(".\\resource")
    return os.path.join(base_path, relative_path)

#PATHS
brick_absent_image_path = "extra_crate.png"
brick_paths = ["extra_character_a.png","extra_character_b.png","extra_character_c.png","extra_character_d.png","extra_character_e.png"]
background_11_path = "Whack_A_Brick_background11.png"
background_169_path = "Whack_A_Brick_background169.jpeg"
braxton_image_path = "braxton-remove.png"
quit_button_image_path = "Quit_Button.png"
quit_button_hover_image_path = "Quit_Button_Hover.png"
start_button_image_path = "StartButton.png"
start_button_hover_image_path = "StartButtonHover.png"
shop_button_image_path = "ShopButton.png"
shop_button_hover_image_path = "ShopButtonHover.png"
shop_back_button_image_path = "BackButton.png"
shop_back_button_hover_image_path = "BackButtonHover.png"
shop_background_image_path = "ShopBackground.jpeg"
background_music_path = "Break_the_Wall.mp3"
settings_image_path = "settings.png"
amongus_sound_path = 'among-us-roundstart.mp3'
cheese_sound_path = 'cheese.mp3'
cursor_image_path = "cursor.png"

# Sounds we want to use
pygame.mixer.init()
braxton_sound = pygame.mixer.Sound(resource_path(amongus_sound_path))
moe_sound = pygame.mixer.Sound(resource_path(cheese_sound_path))
background_music = pygame.mixer.music.load(resource_path(background_music_path))
pygame.mixer.music.play(-1)

# set up the display
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN,pygame.NOFRAME)
infoObject = pygame.display.Info()
desktop_width = infoObject.current_w
desktop_height = infoObject.current_h
print(infoObject)
pygame.display.set_caption("Whack A' Brick!")

def image_loader(image_path, dimension, alpha=True):
    if alpha:
        return pygame.transform.scale(pygame.image.load(resource_path(image_path)).convert_alpha(),dimension)
    else:
        return pygame.transform.scale(pygame.image.load(resource_path(image_path)).convert(),dimension)
#IMAGES
brickabsent = image_loader(brick_absent_image_path,(90,90))
brick_alive = [(state,image_loader(brick_img,(90,90))) for state,brick_img in zip(brickPossibleConfig,brick_paths)]
background_image = image_loader(background_169_path,(desktop_width,desktop_height),False)
shop_background_image = image_loader(shop_background_image_path,(desktop_width,desktop_height),False)
settings_image = pygame.image.load(resource_path(settings_image_path)).convert_alpha()

#Braxton
braxton_x = 612//4
braxton_y = 408//4
braxton_image = pygame.transform.scale(pygame.image.load(resource_path(braxton_image_path)).convert_alpha(),(braxton_x,braxton_y))
braxton_Rect = braxton_image.get_rect()
braxton_Rect.topleft = (0, desktop_height-braxton_y)
screen.blit(background_image, (0, 0))
screen.blit(braxton_image, braxton_Rect)

# Brick class
class Brick(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        orginal_x = 128
        orginal_y = 128
        ratio = 90/orginal_x
        after_x = int(orginal_x*ratio)
        after_y = int(orginal_y*ratio)
        self.image = image_loader(brick_absent_image_path,(after_x,after_y))
        self.rect = Rect(x+70,y-10,after_x,after_y)
        self.status = brickState.ABSENT
        self.absent_image = brickabsent
        self.alive_image = brickabsent
        self.fading = False
        self.fade_alpha = 255
        self.original_image = None
    
    def update(self):
        if self.fading:
            self.fade_alpha -= 10  # Adjust this value to control fade speed (higher = faster fade)
            if self.fade_alpha <= 0:
                self.status = brickState.ABSENT
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
if True:
    pink = (255,157,195)
    white = (255,255,255)
    black = (0, 0, 0)
    lightblue = (30,144,255)
    darkblue = (0,0,139)
    red = (255,0,0)
    blue = (102,102,255)

# create our bricks
if True:
    bricks = [[None for _ in range(5)] for _ in range(5)]
    x = 274
    y = 154
    for i in range(5):
        for j in range(5):
            bricks[i][j] = Brick(x,y) #type: ignore
            x += 274
        x = 274
        y += 154

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


# draw bricks 
allbricks = Group(bricks) #type: ignore
allbricks.draw(screen)

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

def caclculate_score(current_score,buffs):
    value = 1
    for buff in buffs:
        if BUFF.X2SCOREMULTIPLIER == buff:value*=2
        elif BUFF.X3SCOREMULTIPLIER == buff:value*=3
        elif BUFF.X4SCOREMULTIPLIER == buff:value*=4
        elif BUFF.X5SCOREMULTIPLIER == buff:value*=5
        elif BUFF.X6SCOREMULTIPLIER == buff:value*=6
        elif BUFF.X7SCOREMULTIPLIER == buff:value*=7
        elif BUFF.X8SCOREMULTIPLIER == buff:value*=8
        elif BUFF.X9SCOREMULTIPLIER == buff:value*=9
        elif BUFF.X10SCOREMULTIPLIER == buff:value*=10
    return current_score + value


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
            if gameState==GameState.GAME_START:
                for i in range(5):
                    for j in range(5):
                        # if brick was absent, randomly makeit alive
                        aliveodds = 20
                        absentodds = 3
                        if bricks[i][j].status not in brickPossibleConfig and bricks[i][j].fading == False:
                            r = random.randint(1,aliveodds)
                            if r == 1:
                                selected = random.choice(brick_alive)
                                bricks[i][j].status = selected[0]
                                bricks[i][j].image = selected[1]
                        # if alive, randomly make it absent
                        elif bricks[i][j].status not in [brickState.ABSENT,brickState.DEAD]:
                            r = random.randint(1, absentodds)
                            if r == 1:
                                bricks[i][j].status = brickState.ABSENT
                                bricks[i][j].image = bricks[i][j].absent_image

        for i in range(5):
            for j in range(5):
                bricks[i][j].update()


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
                # When shop's back button is clicked, changes to MAIN_MENU
                case GameState.SHOP:
                    if shopBackButtonRect.colliderect(cursor_Rect):
                        gameState = GameState.MAIN_MENU
                case GameState.GAME_START:
                    if startBackButtonRect.colliderect(cursor_Rect):
                        gameState = GameState.MAIN_MENU

                    
                    #when moe is clicked, make it fade, play sound, increase pointsfor i in range(5):
                    for i in range(5):
                        for j in range(5):
                            brick = bricks[i][j]
                            if brick.status in brickPossibleConfig and brick.rect.colliderect(cursor_Rect):
                                brick.status = brickState.DEAD
                                brick.fading = True
                                brick.fade_alpha = 255
                                brick.original_image = brick.image.copy()
                                moe_sound.play()
                                playerPoints = caclculate_score(playerPoints, buffs)

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
                for brick in allbricks:
                    if brick.status in brickPossibleConfig and brick.rect.colliderect(cursor_Rect):
                        brick.status = brickState.DEAD
                        brick.fading = True
                        brick.fade_alpha = 255
                        brick.original_image = brick.image.copy()
                        moe_sound.play()
                        playerPoints += 1

            for brick in allbricks:
                if brick.status in brickPossibleConfig or brick.status == brickState.DEAD:
                    screen.blit(brick.image, brick.rect)
            #draw braxton
            screen.blit(braxton_image, braxton_Rect)

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

            #when braxton is clicked, play sound
            if braxton_Rect.colliderect(cursor_Rect):
                braxton_sound.play()

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

            screen.blit(braxton_image, braxton_Rect)
            screen.blit(quitButtonCurrentImage, quitButtonRect)
            screen.blit(shopButtonCurrentImage, shopButtonRect)
            screen.blit(startButtonCurrentImage, startButtonRect)
            screen.blit(settingsButton,settingsButtonRect)
            pygame.draw.rect(screen, blue, settingsButtonRect, 5)

        # pygame.draw.rect(screen, (0,255,0), startButtonRect, 2)  # green outline
        # pygame.draw.rect(screen, (255,0,0), quitButtonRect, 2)   # red outline
        # pygame.draw.rect(screen, (0,0,255), shopButtonRect, 2)   # blue outline
    for i in range(5):
        for j in range(5):
            pygame.draw.rect(screen, (0,0,255), bricks[i][j].rect, 2)
        #update the display
    screen.blit(cursor_image, cursor_Rect)
    pygame.display.update()