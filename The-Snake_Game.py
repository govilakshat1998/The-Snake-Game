import pygame
import time
import random


pygame.init()


#Defining all required colours 
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)

#Defining the dimensions of the display
display_width = 800
display_height = 600

#defining each block's size
block_size = 10

#Defining the font object from pygame
font = pygame.font.SysFont(None, 25)
img = pygame.image.load('snakehead.png')

#Interactive menu
user_name = raw_input("Enter your name->")
print "Hi", user_name, "!"
print """This is our rendition of the classic game 'Snake'.
The objective of the game is to eat the apple using the snake.

The instructions are fairly simple.
The user is required to control the snake using the arrow keys and eat the apple by
moving the snake's head over the apple.

**RULES**
->If you cross the boundary of the screen, you lose.
->If you eat yourself, you lose.
->If you try to move in the opposite direction, you lose.

**IMPORTANT**
Using the mouse,click the window that pops up after starting the game to take control.


"""
#Checking if music exists and if it does, playing it
try:
    pygame.mixer.music.load("Music.mp3")
    pygame.mixer.music.play(-1)
except:
    pass
x = raw_input("Enter any key to start the game.")



user_score = 0
#Making the 'snake' a class with necessary attributes and methods
class Snake:
    BlockSize = 10
    def __init__(self):
        self.snakeList = []
        self.snakeLength = 0
        self.lead_x = display_width/2
        self.lead_y = display_height/2
    def snake(self):
        #rotating the head of snake according to which direction the snake is moving
        if direction == "right":
            head = pygame.transform.rotate(img,270)
        if direction == "left":
            head = pygame.transform.rotate(img,90)
        if direction == "up":
            head = img
        if direction == "down":
            head = pygame.transform.rotate(img,180)
        #Displaying the snake onto the screen
        gameDisplay.blit(head, (self.snakeList[-1][0],self.snakeList[-1][1]))
        for XnY in self.snakeList[:-1]:
            pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],Snake.BlockSize,Snake.BlockSize])  

#Creating a score class. Each object of the class controls the score
class Score:
    def __init__(self):
        self.score = 0
        self.snakeLength = 0
    def score_show(self):
        text = font.render("Score: "+str(self.score), True, white)
        gameDisplay.blit(text,[0,0])

#Function to display message to the screen
def message_to_screen(msg,colour):
    screen_text = font.render(msg, True, colour)
    gameDisplay.blit(screen_text, [display_width/2-300, display_height/2])



#Defining the surface object with caption
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('The Snake Game')

clock = pygame.time.Clock()
logo = pygame.image.load("logo.png")
gameDisplay.blit(logo, (275,75))

msg = """Welcome to the snake game!"""

screen_text = font.render(msg, True, white)
gameDisplay.blit(screen_text, [display_width/2 - 100, display_height/2+50])
pygame.display.update()
time.sleep(3)

def gameLoop():
    #Main loop of the gam
    global user_name
    global user_score
    apple = pygame.image.load("apple.png")
    global direction
    FPS = 25
    gameExit = False
    gameOver = False
    #lead_change variables control the amount by which the snake head's coordinates change
    lead_x_change = 10
    lead_y_change = 0
    direction = "right"
    SNAKE = Snake()
    SNAKE.snakeLength = 1

    sc = Score()

    #Generating random coordinates for the apple
    randAppleX = round(random.randint(0,display_width-block_size)/10.0)*10
    randAppleY = round(random.randint(0,display_height-block_size)/10.0)*10
    #This loop runs as long as the user decides to continue
    
    while not gameExit:
        #This loop runs when game over condition is satisfied
        while gameOver == True:
            #obtaining old high score from external file
            f= open("highscore.txt",'r')
            g = f.readlines()
            #checking if new high score has been set
            if sc.score > int(g[1]):
                tmp = "CONGRATULATIONS, YOU BEAT "+str(g[0])+" WITH A NEW RECORD OF "+str(sc.score)
                message_to_screen(tmp,red)
                pygame.display.update()
                #slowing down the display time
                time.sleep(3)
                gameDisplay.fill(black)
                tmp =  "Saving...."
                message_to_screen(tmp,red)
                pygame.display.update()
                gameDisplay.fill(black)
                time.sleep(1)
                tempL = [str(user_name)+"\n",str(sc.score)]
                f.close()
                #if highscore has been beaten, writing it into the external file
                f= open("highscore.txt",'w')
                f.writelines(tempL)
                f.close()
                tmp = "Saved."
                message_to_screen(tmp,red)
                pygame.display.update()
                gameDisplay.fill(black)
                #giving the user the option to either play again or quit the game
                tmp = "PRESS C TO PLAY AGAIN OR Q TO QUIT"
                message_to_screen(tmp,red)
            else:
                #Screen to be displayed if high score is not obtained
                gameDisplay.fill(black)
                tempMes = "GAME OVER    Score " + str(sc.score) + "    PRESS C TO PLAY AGAIN OR Q TO QUIT"
                message_to_screen(tempMes, red)
                pygame.display.update()
            #This loops checks the user's input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
        #This loop monitors user events and inputs and makes neccessary changes to variables
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -10
                    lead_y_change = 0
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = 10
                    lead_y_change = 0
                    direction = "right"
                elif event.key == pygame.K_UP:
                    lead_y_change = -10
                    lead_x_change = 0
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    lead_y_change = 10
                    lead_x_change = 0
                    direction = "down"
        #If the snake crosses the boundary of the window, gameOver is set to True
        if SNAKE.lead_x >= display_width or SNAKE.lead_x < 0 or SNAKE.lead_y >= display_height or SNAKE.lead_y < 0:
            gameOver = True

        SNAKE.lead_x += lead_x_change
        SNAKE.lead_y += lead_y_change
        gameDisplay.fill(black)
        #pygame.draw.rect(gameDisplay, red, [randAppleX,randAppleY,block_size,block_size])
        gameDisplay.blit(apple, (randAppleX,randAppleY))#generates the apple
        #Appending coordinates of all snake segments to its list
        snakeHead = []      
        snakeHead.append(SNAKE.lead_x)
        snakeHead.append(SNAKE.lead_y)
        SNAKE.snakeList.append(snakeHead)
        #Deleting redundant segments
        if len(SNAKE.snakeList) > SNAKE.snakeLength:
            del SNAKE.snakeList[0]
        #Checking if the snake is eating itself
        for eachSegment in SNAKE.snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
        #Displaying the snake, score and updating the screen
        SNAKE.snake()
        sc.score_show()
        pygame.display.update()
        #Checking if the snake has crossed or eaten the apple
        if SNAKE.lead_x >= randAppleX and SNAKE.lead_x <= randAppleX + 10 or SNAKE.lead_x + 10 <= randAppleX and SNAKE.lead_x + 10 >= randAppleX:
            if SNAKE.lead_y >= randAppleY and SNAKE.lead_y <= randAppleY + 10 or SNAKE.lead_y + 10<= randAppleY and SNAKE.lead_y + 10 >= randAppleY:
                randAppleX = round(random.randint(0,display_width-block_size)/10.0)*10
                randAppleY = round(random.randint(0,display_height-block_size)/10.0)*10
                SNAKE.snakeLength += 1
                sc.score += 1
                FPS +=2
        clock.tick(FPS)
    pygame.quit()
    quit()
#gameLoop()
try:
    gameLoop()
except Exception, e:
    print e.message

