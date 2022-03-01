# PyPong
import pygame
from sys import exit
import random


def ball_animation(): # ball animation function created to keep game loop code clean
    # ball movement variables; declared globally so they can be used outside of the function only declare globally with simple code, better alternatives: utilizing return statements or use a class
    global bspeed_x, bspeed_y, p_score, o_score, score_time
    ball.x += bspeed_x
    ball.y += bspeed_y

    # checks for ball out of bounds, checks use <= instead of == because the ball moves 7 per frame, ex: if it was 5 from the boundary the cyclewould allow it to pass through the boundary 
    if ball.top <= 0 or ball.bottom >= screen_h:
        bspeed_y *=-1 # reverse ball y if it hits boundaries

    if ball.left <= 0: # check if ball goes plast the player
        p_score +=1 # updates player score and resets ball
        
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_w: # check if ball went past the opponent
        o_score +=1
        
        score_time = pygame.time.get_ticks()
    
    # collisions: check if the ball connects to either the palyer or the opponent and reverses the horizontal movement
    if ball.colliderect(player1) or ball.colliderect(opponent):
        bspeed_x *= -1


def player_animation():
    player1.y += player_speed

    if player1.top <= 0:
        player1.top = 0
    if player1.bottom >= screen_h:
        player1.bottom = screen_h


def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_h:
        opponent.bottom = screen_h


def ball_restart():
    global bspeed_x, bspeed_y, score_time

    current_time = pygame.time.get_ticks() # gives what time we are on right now as opposed to the timer in ball_animation that runs once
    ball.center = (screen_w/2, screen_h/2)


    if current_time - score_time < 700: # subtracts current time from game time in order to give us a timer effect
        number_three = game_font.render("3",False,light_grey)
        screen.blit(number_three,(screen_w/2-10,screen_h/2+100))
    if 700 < current_time - score_time < 1400:
        number_three = game_font.render("2",False,light_grey)
        screen.blit(number_three,(screen_w/2-10,screen_h/2+100))
    if 1400 < current_time - score_time < 2100:
        number_three = game_font.render("1",False,light_grey)
        screen.blit(number_three,(screen_w/2-10,screen_h/2+100))
    
    if current_time - score_time < 2100:
        bspeed_x, bspeed_y = 0,0
    else:
        bspeed_y = 7 * random.choice((1,-1))
        bspeed_x = 7 * random.choice((1,-1))
        score_time = None # stop score_time from being run


# General setup
pygame.init()
clock = pygame.time.Clock()


# setting up display
screen_w = 1000
screen_h = 650
screen = pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption('PyPong')
ball_surf = pygame.image.load('Pyrunner/Graphics/HUD/hud_p1.png').convert_alpha()


# game rectangles
ball = ball_surf.get_rect(center = (screen_w/2, screen_h/2)) # places ball in center of screen
player1 = pygame.Rect(10, screen_h/2-70, 10, 140) # places player rect on the left at the center of the height
opponent = pygame.Rect(screen_w - 20, screen_h/2-70, 10, 140) # rect for opponent


# colors used
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)


# speed variables
bspeed_x = 7 * random.choice((1,-1))
bspeed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7


# text variables
p_score = 0
o_score = 0
game_font = pygame.font.Font('Pyrunner/Pixeltype.ttf', 50)


# Score Timer
score_time = True




# game loop
while True:
    # input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed +=7


    # calling functions that control animation of screen objects
    ball_animation()
    player_animation()
    opponent_ai()


    # Visuals drawn into the display
    screen.fill(bg_color) # fill display with background color
    pygame.draw.rect(screen,light_grey, player1) # draw player
    pygame.draw.rect(screen, light_grey, opponent) # draw opponent
    screen.blit(ball_surf, ball)# draw the ball
    pygame.draw.aaline(screen, light_grey,(screen_w/2,0),(screen_w/2,screen_h)) # draw mid line of the game
    # note: order is important when drawing, things at the top of the order are drawn first and the others then go above that
    
    if score_time:
        ball_restart() # extracted from ball_animation so that it is fun every frame instead of once, this way it can interact with the start_time and other functions that are called once


    player_text = game_font.render(f"{p_score}", False, light_grey) # creates player score object
    screen.blit(player_text, (450,50)) # uses blit to draw the player score
    
    opp_text = game_font.render(f"{o_score}", False, light_grey) 
    screen.blit(opp_text, (530,50))


    # window updating per frame
    pygame.display.flip() # uses flip instead of update; update updates part of the screen while flip updates/'redraws' the entire screen
    clock.tick(60)


