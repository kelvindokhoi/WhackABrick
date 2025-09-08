# STARTER
from pygame import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os
from pygame.locals import *
import random

# need for making .exe later
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS #type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#PATHS
mole_absent_image_path = "moe-remove.png"
hole_image_path = "mario_pipe_2-remove.png"
background_path = "background.jpg"
braxton_image_path = "braxton-remove.png"

# Sounds we want to use
pygame.mixer.init()
braxton_sound = pygame.mixer.Sound('among-us-roundstart.mp3')
moe_sound = pygame.mixer.Sound('cheese.mp3')

# set up the display
pygame.init()
screen = pygame.display.set_mode((700,700),pygame.NOFRAME)
pygame.display.set_caption("Whack a Moe!")

#IMAGES
moleabsent = transform.scale(image.load(resource_path(hole_image_path)).convert_alpha(),(90,30))
background_image = transform.scale(image.load(resource_path(background_path)).convert(),(700,700))
braxton_x = 612//4
braxton_y = 408//4
braxton_image = transform.scale(image.load(resource_path(braxton_image_path)).convert_alpha(),(braxton_x,braxton_y))
screen.blit(background_image, (0, 0))
screen.blit(braxton_image, (0, 700-408//4))

# Mole class
class Mole(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        orginal_x = 431
        orginal_y = 579
        ratio = 60/orginal_x
        after_x = int(orginal_x*ratio)
        after_y = int(orginal_y*ratio)
        self.image = transform.scale(image.load(resource_path(mole_absent_image_path)).convert_alpha(),(after_x,after_y))
        self.rect = self.image.get_rect().move(x+10,y-10)
        # self.rect = self.image.get_rect().move(x,y)
        self.status = 'absent'
        self.absent_image = transform.scale(image.load(resource_path(mole_absent_image_path)).convert_alpha(),(after_x,after_y))
        self.alive_image = transform.scale(image.load(resource_path(mole_absent_image_path)).convert_alpha(),(after_x,after_y))
        self.dead_image = image.load(resource_path("moledead.png")).convert()

# for timing
framerate = 1000  # you can modify to adjust speed of animation, 1 second = 1000 milliseconds
TIMEREVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEREVENT, framerate)

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

        if event.type == TIMEREVENT:
            # this means our timer went off!
            # randomly set moles to be up or down
            if gameStarted:
                for i in range(5):
                    for j in range(5):
                        # if mole was absent, randomly makeit alive
                        aliveodds = 20
                        absentodds = 3
                        if moles[i][j].status == 'absent':
                            r = random.randint(1,aliveodds)
                            if r == 1:
                                moles[i][j].status = 'alive'
                                moles[i][j].image = moles[i][j].alive_image
                        # if alive, randomly make it absent
                        elif moles[i][j].status == 'alive':
                            r = random.randint(1, absentodds)
                            if r == 1:
                                moles[i][j].status = 'absent'
                                moles[i][j].image = moles[i][j].absent_image

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
            
            #play amongus sound when braxton is clicked
            braxton_pos_x1 = 0
            braxton_pos_x2 = 0 + braxton_x
            braxton_pos_y1 = 700-408//4
            braxton_pos_y2 = 700

            if braxton_pos_x1<=mousex<=braxton_pos_x2 and braxton_pos_y1<=mousey<=braxton_pos_y2:
                braxton_sound.play()

            #play cheese when moe is clicked
            if any(a_moe.status=="alive" and a_moe.rect.collidepoint(mousePos) for a_moe in allmoles):
                moe_sound.play()


        # paint the background
        # screen.fill(pink)
        screen.blit(background_image, (0, 0))

        # draw the header
        pygame.draw.rect(screen, pink, headerRect)
        screen.blit(headerText, headerRect)

        # draw the moles
        for a_mole in allmoles:
            if a_mole.status!="absent":
                screen.blit(a_mole.image,a_mole.rect)
        # allmoles.draw(screen)
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

#######################################

# random appearance with animation
import random
from pygame import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os
from pygame.locals import *

# need for making .exe later
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS #type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Colors we want to use
pink = (255,157,195)
white = (255,255,255)
black = (0, 0, 0)
lightblue = (30,144,255)
darkblue = (0,0,139)
red = (255,0,0)

# Sounds we want to use
pygame.mixer.init()
hitsound = pygame.mixer.Sound('hit.wav')

# set up the display
pygame.init()
screen = pygame.display.set_mode((700,700))
pygame.display.set_caption("Whack a Mole!")
screen.fill(pink)

moleabsent = image.load(resource_path("molehole.png")).convert()
molealive = image.load(resource_path("molealive.png")).convert()
moledead = image.load(resource_path("moledead.png")).convert()

# Mole class
class Mole(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = moleabsent
        self.rect = self.image.get_rect().move(x,y)
        self.status = 'absent'

# for timing
framerate = 1000  # you can modify to adjust speed of animation, 1 second = 1000 milliseconds
TIMEREVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEREVENT, framerate)

# create our moles
moles = [[None for _ in range(5)] for _ in range(5)]
x = 100
y = 100
for i in range(5):
    for j in range(5):
        moles[i][j] = Mole(x,y)
        x += 100
    x = 100
    y += 100

# create some fonts
headerfont = Font('freesansbold.ttf', 48)
buttonfont = pygame.font.SysFont('Corbel',32)
buttonfont.set_bold(True)

# create some text
headerText = headerfont.render("Whack 'A Mole!", True, black, pink)
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

allmoles = Group(moles)
allmoles.draw(screen)
gameStarted = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == TIMEREVENT:
            # this means our timer went off!
            # randomly set moles to be up or down
            if gameStarted:
                for i in range(5):
                    for j in range(5):
                        # if mole was absent, randomly makeit alive
                        aliveodds = 20
                        absentodds = 3
                        if moles[i][j].status == 'absent':
                            r = random.randint(1,aliveodds)
                            if r == 1:
                                moles[i][j].status = 'alive'
                                moles[i][j].image = molealive
                        # if alive, randomly make it absent
                        elif moles[i][j].status == 'alive':
                            r = random.randint(1, absentodds)
                            if r == 1:
                                moles[i][j].status = 'absent'
                                moles[i][j].image = moleabsent


        # find mouse position
        mousePos = pygame.mouse.get_pos()
        mousex = mousePos[0]
        mousey = mousePos[1]
        # print(mousex,mousey)

        if event.type == pygame.MOUSEBUTTONDOWN:
            # was the quit rectangle clicked?
            if not gameStarted and mousex >= quitButtonx and mousex <= quitButtonx + quitButtonwidth and \
                    mousey >= quitButtony and mousey <= quitButtony + quitButtonheight:
                pygame.quit()
                sys.exit()
            if not gameStarted and mousex >= startButtonx and mousex <= startButtonx + startButtonwidth and \
                mousey >= startButtony and mousey <= startButtony + startButtonheight:
                gameStarted = True
                pygame.mouse.set_visible(False)
                cursor_image = pygame.image.load("hammer.png")
                cursor_rect = cursor_image.get_rect()

        # paint the background
        screen.fill(pink)

        # draw the header
        pygame.draw.rect(screen, pink, headerRect)
        screen.blit(headerText, headerRect)

        # draw the moles
        allmoles.draw(screen)

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

        #update the display
        pygame.display.update()