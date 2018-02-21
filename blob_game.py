# The Blob game
# Peter Ferjancic, February 2018

# GNU All-Permissive License
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

import pygame
import sys
import os

import random

'''
------======XXXXXXXX======------
            OBJECTS
------======XXXXXXXX======------
'''

class Player(pygame.sprite.Sprite):
    '''
    Spawn a player
    '''
    def __init__(self):
        # initiation parameters
        pygame.sprite.Sprite.__init__(self)

        # movement parameters
        self.speedx = 0
        self.speedy = 0
        self.speedxTrgt = 0
        self.speedyTrgt = 0

        # animation parameters
        self.frame = 0
        self.images = []
        for i in range(1,5):
            img = pygame.image.load(os.path.join('images','hero' + str(i) + '.png')).convert()
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)
            self.image = self.images[0]
            self.rect  = self.image.get_rect()
        self.rect.x = worldx/2 - 20
        self.rect.y = worldy/2 - 20
        
        # other 
        self.score=0

    # -- METHOD: set new movement speeds
    def controlLR(self,x):
        self.speedxTrgt = x
    def controlUD(self,y):    
        self.speedyTrgt = y

    # -- METHOD: set to new position
    def update(self):
        # Calcuate new target speed (acceleration and whatnot)
        self.speedx= self.speedx + 0.02*(self.speedxTrgt-self.speedx)
        self.speedy= self.speedy + 0.02*(self.speedyTrgt-self.speedy)
        # set speed to 0 once slowed down enough.
        if abs(self.speedx) < 0.6 and self.speedxTrgt == 0 and abs(self.speedy) < 0.6 and self.speedyTrgt == 0:
            self.speedx =0
            self.speedy =0
        # update self position
        self.rect.x = self.rect.x + self.speedx
        self.rect.y = self.rect.y + self.speedy

        # animating the movement
        if self.speedx != 0 or self.speedy != 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = self.images[self.frame//ani]
        else:
            self.frame = 0
            self.image = self.images[self.frame//ani]

        # walls
        SideBuff=40
        if self.rect.x < 0:
            self.rect.x =0
            self.speedx =-0.5 * self.speedx

        if self.rect.x > worldx - SideBuff:
            self.rect.x = worldx - SideBuff
            self.speedx =-0.5 * self.speedx

        if self.rect.y < 0:
            self.rect.y = 0
            self.speedy =-0.5 * self.speedy

        if self.rect.y > worldy - SideBuff:
            self.rect.y = worldy - SideBuff
            self.speedy =-0.5 * self.speedy
            

    # -- METHOD: increase score
    def scoreInc(self, increase):
        self.score += increase


class ScoreNew():
    # class to keep track of and display score.
    def __init__(self):
        self.myfont = pygame.font.SysFont(None, 24)
        self.value=0

        self.scoreString = 'Score: '+ str(self.value) # calculate updated score
        self.textsurface = self.myfont.render(self.scoreString, True, (255, 255, 255)) # redraw updated
        self.textrect = self.textsurface.get_rect()
        self.textrect.centerx = worldx-80
        self.textrect.centery = 30

    def inc(self, increase):
        self.value += increase

        self.scoreString = 'Score: '+ str(self.value) # calculate updated score
        self.textsurface = self.myfont.render(self.scoreString, True, (255, 255, 255)) # redraw updated

class GameTimer():
    # class to keep track of and display score.
    def __init__(self, startTime):
        self.myfont = pygame.font.SysFont(None, 24)
        self.value=startTime

        self.scoreString = 'Time left: '+ str(self.value) # calculate updated score
        self.textsurface = self.myfont.render(self.scoreString, True, (255, 255, 255)) # redraw updated
        self.textrect = self.textsurface.get_rect()
        self.textrect.centerx = 80
        self.textrect.centery = 30

    def update(self, change):
        self.value += change

        self.scoreString = 'Time left: '+ str(self.value) # calculate updated score
        self.textsurface = self.myfont.render(self.scoreString, True, (255, 255, 255)) # redraw updated

        if self.value >0:
            over=0
        else:
            over=1
        return over


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, r):
        # initiation parameters
        pygame.sprite.Sprite.__init__(self)

        # animation parameters
        self.frame = 0
        self.images = []
        img = pygame.image.load(os.path.join('images','obstacle.png')).convert()
        img.convert_alpha()
        img.set_colorkey(ALPHA)
        self.images.append(img)
        self.image = self.images[0]
        self.rect  = self.image.get_rect()

        w,h = self.image.get_size()
        # print(str(w) + str(h))
        self.image = pygame.transform.scale(self.image, (int(w*r), int(h*r)))

        self.rect.x=x
        self.rect.y=y


'''
------======XXXXXXXX======------
        FUNCTIONS
------======XXXXXXXX======------
'''
def gen_newFood():
    x = random.randint(40, worldx-40)
    y = random.randint(40, worldy-40)
    r = random.random()*0.8+0.2
    global foodOne
    global food_list
    foodOne = Obstacle(x, y, 0.5)   
    food_list = pygame.sprite.Group()
    food_list.add(foodOne)




'''
------======XXXXXXXX======------
              SETUP
------======XXXXXXXX======------
'''
pygame.init()
pygame.font.init()

# window size
worldx = 960
worldy = 720
fps = 60        # frame rate
ani = 4         # animation cycles
clock = pygame.time.Clock()
mainLoop = True     # run main loop

BLUE  = (25,25,200)
BLACK = (23,23,23)
WHITE = (254,254,254)
ALPHA = (0,255,0)

speed = 20      # how fast to move
myTime = 0      # time difference
remainingTime = 30 # how much time does the player have left

# create the playing window
screen = pygame.display.set_mode([worldx,worldy])
pygame.display.set_caption('The Blob Game')
backdrop = pygame.image.load(os.path.join('images','stage.png')).convert()
backdropbox = screen.get_rect()

gameOverfontBIG = pygame.font.SysFont(None, 48)
gameOverfontMED = pygame.font.SysFont(None, 36)

# initialize the Player class (spawn player)
playerMe = Player()   
player_list = pygame.sprite.Group()
player_list.add(playerMe)

# init score counter
playerScore = ScoreNew()

# init timer
playerTimer = GameTimer(30)

# initialize the Food class (create obstacle blob)
gen_newFood()

# "state machine" 
RUNNING   = True
PAUSED    = False 
GAME_OVER = False


'''
------======XXXXXXXX======------
              MAIN
------======XXXXXXXX======------
'''
while mainLoop == True:

    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                mainLoop = False

            # --- Key press events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    playerMe.controlLR(-speed)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    playerMe.controlLR(speed)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    playerMe.controlUD(-speed)
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    playerMe.controlUD(speed)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    playerMe.controlLR(0)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    playerMe.controlLR(0)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    playerMe.controlUD(0)
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    playerMe.controlUD(0)

                if event.key == ord('q'):
                    pygame.quit()
                    sys.exit()
                    mainLoop = False

    #    world.fill(BLACK)
        screen.blit(backdrop, backdropbox)
        # update player score
        screen.blit(playerScore.textsurface, playerScore.textrect)
        # update player timer
        screen.blit(playerTimer.textsurface, playerTimer.textrect)
        # update player timer

        playerMe.update()           # calculate the new position of player
        food_list.draw(screen)      # draw new obstacle position
        player_list.draw(screen)    # draw new player position

        hit = pygame.sprite.spritecollide(playerMe, food_list, False)
            # first parameter takes a single sprite
            # second parameter takes sprite groups
            # third parameter is a do kill commad if true
            # all group objects colliding with the first parameter object will be
            # destroyed. The first parameter could be bullets and the second one
            # targets although the bullet is not destroyed but can be done with
            # simple trick bellow
        if hit:
            # the objects are close! time to compare them better
            hit2=pygame.sprite.collide_mask(playerMe,foodOne)
            if hit2:
                playerScore.inc(1)
                foodOne.kill()
                gen_newFood()

        pygame.display.flip()
        dt=clock.tick(fps)
        myTime += dt
        if myTime>1000:
            myTime=myTime-1000
            gOver = playerTimer.update(-1)
            if gOver:
                print('Game over!')
                RUNNING   = False
                GAME_OVER = True
    


    while GAME_OVER:
        screen.blit(backdrop, backdropbox)
        
        textGO1 = gameOverfontBIG.render("Game Over", True, WHITE)
        text_rect = textGO1.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(textGO1, [text_x, text_y])

        textGO2 = gameOverfontMED.render("Your final score: " + str(playerScore.value), True, WHITE)
        text_rect = textGO2.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = text_y + 30
        screen.blit(textGO2, [text_x, text_y+30])


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                mainLoop = False
            if event.type == pygame.KEYUP:
                if event.key == ord('q'):
                    pygame.quit()
                    sys.exit()
                    mainLoop = False

        pygame.display.flip()




