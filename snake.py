# Simple snake game made using python and pygame

import sys, pygame
import random
from pygame.locals import *
pygame.init()
pygame.font.init()

# Creating a clock for the in game frame counter
clock = pygame.time.Clock()

# creating the colors and the size of the screen
black = 0,0,0
green = 0,255,0
red = 255,0,0
size = [800, 600]

# create event ideas for my 2 user defined events
move_snake = pygame.USEREVENT + 1
place_apple = pygame.USEREVENT + 2

# set the global snake movement speed and apple respawn speed
SNAKE_SPEED = 250
APPLE_SPEED = 10000

# initialize the score to zero
score = 0

# initialize the fonts used and the display surfaces
losefont = pygame.font.Font('freesansbold.ttf', 50)
scorefont = pygame.font.Font('freesansbold.ttf', 20)
textsurface = losefont.render('You Lose', False, green)
scoresurface = scorefont.render('Score: 0', False, green)
screen = pygame.display.set_mode(size)

# create the snake class used to hold and modify the snake data
class Snake:
    # initializing and defining the instance variables
    def __init__(self):
        self.x_pos = 100
        self.y_pos = 100
        self.pos = (self.x_pos, self.y_pos)
        self.dir = 'right'
        self.length = 1
        self.locs = [(100,100)]
    

    # the move method that causes the snake to move across the screen
    def move(self):
        if self.dir == 'right':
            self.x_pos = self.x_pos + 25
        elif self.dir == 'up':
            self.y_pos = self.y_pos - 25
        elif self.dir == 'down':
            self.y_pos = self.y_pos + 25
        elif self.dir == 'left':
            self.x_pos = self.x_pos - 25
        self.pos = (self.x_pos, self.y_pos)
        self.locs.insert(0, self.pos)
        self.locs.pop()

# method for randomly placing the apple on the screen    
def put_apple(locs):
    x_pos = random.randint(0,32)*25
    y_pos = random.randint(0,24)*25
    while [x_pos, y_pos] in locs:
        x_pos = random.randint(0,32)*25
        y_pos = random.randint(0,24)*25
    return (x_pos, y_pos)

# create a snake object for use in the game loop
snake = Snake()

# set the starting position of the apple
apple_pos = put_apple(snake.locs)

# start timed loops for the snake moving event, and the apple respawn event
pygame.time.set_timer(move_snake, SNAKE_SPEED)
pygame.time.set_timer(place_apple, APPLE_SPEED)     

# initialize the losing variable, use to decide when to display the losing screen
lose = False

# game loop
while 1:
    if not lose:
        # set frame rate to 30 fps
        msElapsed = clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # check to see what direction to move
            elif event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    snake.dir = 'up'
                elif event.key == K_a:
                    snake.dir = 'left'
                elif event.key == K_s:
                    snake.dir = 'down'
                elif event.key == K_d:
                    snake.dir = 'right'
            elif event.type == move_snake:
                snake.move()
                # check to see if the snake is running into itself
                if snake.pos in snake.locs[1:]:
                    lose = True
                # check to see if the snake runs off the screen
                if snake.x_pos < 0 or snake.x_pos > 800 or snake.y_pos < 0 or snake.y_pos > 600:
                    lose = True
            elif event.type == place_apple:
                apple_pos = put_apple(snake.locs)
        # clear the screen to prepare to draw
        screen.fill(black)
        # check to see if snake is eating apple
        if snake.pos == apple_pos:
            # add another square to the snake, then increment the score
            snake.locs.insert(0,apple_pos)
            snake.length = snake.length + 1
            apple_pos = put_apple(snake.locs)
            score = score + 1
            scoresurface = scorefont.render('Score:'+str(score), False, (0, 255, 0))
        pygame.draw.rect(screen, red, (apple_pos[0]+7, apple_pos[1]+7, 10, 10), 0)
        # draw all the squares in the body of the snake
        for loc in snake.locs:
            pygame.draw.rect(screen, green, (loc[0], loc[1], 25, 25), 0)
        # draw score
        screen.blit(scoresurface, (0,0))
        pygame.display.flip()


    elif lose:
        # display lose screen, handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(black)
        screen.blit(textsurface, (250,200))
        pygame.display.flip()

