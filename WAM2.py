# STARTER
from pygame import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os
from pygame.locals import *
from random import randint

# need for making .exe later
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS #type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#PATHS
mole_image_path = "moe-remove.png"
hole_image_path = "mario_pipe_2-remove.png"
background_path = "background.jpg"
braxton_image_path = "braxton-remove.png"



# Mole class
class Mole(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        orginal_x = 431
        orginal_y = 579
        ratio = 60/orginal_x
        after_x = int(orginal_x*ratio)
        after_y = int(orginal_y*ratio)
        self.image = transform.scale(image.load(resource_path(mole_image_path)).convert_alpha(),(after_x,after_y))
        self.rect = self.image.get_rect().move(x+after_x//2-10,y-10)

class Hole(Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = transform.scale(image.load(resource_path(hole_image_path)).convert_alpha(),(90,30))
        self.rect = self.image.get_rect().move(x,y+50)

# Colors we want to use
pink = (255,157,195)
white = (255,255,255)
black = (0, 0, 0)
lightblue = (30,144,255)
darkblue = (0,0,139)
red = (255,0,0)

# Sounds we want to use
pygame.mixer.init()
braxton_sound = pygame.mixer.Sound('among-us-roundstart.mp3')
moe_sound = pygame.mixer.Sound('cheese.mp3')

# set up the display
pygame.init()
screen = pygame.display.set_mode((700,700),pygame.NOFRAME)
pygame.display.set_caption("Whack a Moe!")
#IMAGES
background_image = transform.scale(image.load(resource_path(background_path)).convert(),(700,700))
braxton_x = 612//4
braxton_y = 408//4
braxton_image = transform.scale(image.load(resource_path(braxton_image_path)).convert_alpha(),(braxton_x,braxton_y))
screen.blit(background_image, (0, 0))
screen.blit(braxton_image, (0, 700-408//4))

# create our moles
moles = [[None for _ in range(5)] for _ in range(5)]
holes = [[None for _ in range(5)] for _ in range(5)]
x = 100
y = 100
for i in range(5):
    for j in range(5):
        holes[i][j] = Hole(x,y) #type: ignore
        moles[i][j] = Mole(x,y) #type: ignore
        x += 100
    x = 100
    y += 100

# create some fonts
headerfont = Font('freesansbold.ttf', 48)
buttonfont = pygame.font.SysFont('Corbel',32)
buttonfont.set_bold(True)

# create some text
headerText = headerfont.render("Whack 'A Moe!", True, black, pink)
headerRect = headerText.get_rect()
headerRect.center = (350,50)
pygame.draw.rect(screen,pink,headerRect)
screen.blit(headerText, headerRect)

# create text and info for our quit button
quitButtonText = buttonfont.render(" Quit ", True, black, pink)
quitButtonRect = quitButtonText.get_rect()
quitButtonx = 200
quitButtony = 600
quitButtonwidth = quitButtonRect.width
quitButtonheight = quitButtonRect.height
quitButtonRect.topleft = (quitButtonx,quitButtony)
pygame.draw.rect(screen,white,quitButtonRect)
screen.blit(quitButtonText, quitButtonRect)

# create text and info for our start button
startButtonText = buttonfont.render(" Start ", True, black, pink)
startButtonRect = startButtonText.get_rect()
startButtonx = 400
startButtony = 600
startButtonwidth = startButtonRect.width
startButtonheight = startButtonRect.height
startButtonRect.topleft = (startButtonx,startButtony)
pygame.draw.rect(screen,white,startButtonRect)
screen.blit(startButtonText, startButtonRect)


allmoles = Group(moles) #type: ignore
allmoles.draw(screen)

allholes = Group(holes) #type: ignore
allholes.draw(screen)

gameStarted = False


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # find mouse position
        mousePos = pygame.mouse.get_pos()
        mousex = mousePos[0]
        mousey = mousePos[1]
        # print(mousex,mousey)

        if event.type == pygame.MOUSEBUTTONDOWN:
            # was the quit rectangle clicked?
            if mousex >= quitButtonx and mousex <= quitButtonx + quitButtonwidth and \
                mousey >= quitButtony and mousey <= quitButtony + quitButtonheight:
                pygame.quit()
                sys.exit()
            
            if not gameStarted and mousex >= startButtonx and mousex <= startButtonx + startButtonwidth and \
                mousey >= startButtony and mousey <= startButtony + startButtonheight:
                gameStarted = True
                pygame.mouse.set_visible(False)
                cursor_image = transform.scale(pygame.image.load("braxton-remove.png"),(60,60))
                cursor_rect = cursor_image.get_rect()

            braxton_pos_x1 = 0
            braxton_pos_x2 = 0 + braxton_x
            braxton_pos_y1 = 700-408//4
            braxton_pos_y2 = 700

            if not gameStarted and braxton_pos_x1<=mousex<=braxton_pos_x2 and braxton_pos_y1<=mousey<=braxton_pos_y2:
                braxton_sound.play()


        # paint the background
        # screen.fill(pink)
        screen.blit(background_image, (0, 0))

        # draw the header
        pygame.draw.rect(screen, pink, headerRect)
        screen.blit(headerText, headerRect)

        # draw the moles
        allmoles.draw(screen)
        allholes.draw(screen)
        screen.blit(braxton_image, (0, 700-408//4))

        if gameStarted:
            cursor_rect.center = pygame.mouse.get_pos()
            screen.blit(cursor_image, cursor_rect)
        else:
            # if hovering on a button, change its color
            if mousex >= quitButtonx and mousex <= quitButtonx + quitButtonwidth and \
                    mousey >= quitButtony and mousey <= quitButtony + quitButtonheight:
                quitButtonText = buttonfont.render(" Quit ", True, red, pink)
            else:
                quitButtonText = buttonfont.render(" Quit ", True, black, pink)

            # draw the quit button text
            screen.blit(quitButtonText, quitButtonRect)

            if mousex >= startButtonx and mousex <= startButtonx + startButtonwidth and \
                    mousey >= startButtony and mousey <= startButtony + startButtonheight:
                startButtonText = buttonfont.render(" Start ", True, red, pink)
            else:
                startButtonText = buttonfont.render(" Start ", True, black, pink)

            # draw the start button text
            screen.blit(quitButtonText, quitButtonRect)
            screen.blit(startButtonText, startButtonRect)

        # if hovering on a button, change its color
        if mousex >= quitButtonx and mousex <= quitButtonx + quitButtonwidth and \
                mousey >= quitButtony and mousey <= quitButtony + quitButtonheight:
            quitButtonText = buttonfont.render(" Quit ", True, red, pink)
        else:
            quitButtonText = buttonfont.render(" Quit ", True, black, pink)

        # draw the button text
        screen.blit(quitButtonText, quitButtonRect)

        #update the display
        pygame.display.update()