#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 23:16:31 2019

@author: jessica
"""
import pygame, random, time
from random import randint
from pygame.locals import *
from pygame.compat import unichr_, unicode_

# Colors
col_white = (250, 250, 250)
col_black = (0, 0, 0)
col_gray = (220, 220, 220)
col_blue = (0, 0, 250)
col_yellow = (250,250,0)

# Initializing global variables
LEFT = 1 #left mouse button
NUM_SQUARES = 9
SQUARE_WIDTH = 100
MARGIN = 100
Squares = [] # List of generated squares
S = 2 # Sequence of length S starting with 2
correct_trials = 0
incorrect_trials = 0 # internal variable that runs from 0 - 2
total_trials = 0

#screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
BACKGR_COL = col_white

    
# Initializing the display
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Corsi Block Tapping Task")
myfont = pygame.font.SysFont('Comic Sans MS', 30)
myfont_small = pygame.font.SysFont('Comic Sans MS', 20)

# Creating the surface
surface = pygame.display.get_surface()
        

def main():

    global S, total_trials, correct_trials, incorrect_trials
    STATE = "welcome"
    pygame.event.clear()

    # main while loop
    while True:

        # event loop
        for event in pygame.event.get():

            # interactive transitionals
            if STATE == "task introduction":
                if event.type == MOUSEBUTTONDOWN and event.button == LEFT:
                    clickpos = pygame.mouse.get_pos()
                    if start_button.collidepoint(clickpos):
                        STATE = "new sequence"

            if STATE == "trial":
                if event.type == MOUSEBUTTONDOWN and event.button == LEFT:
                    i = clicked_square_index() #i=index of clicked square
                    if i >= 0: # square was clicked
                        if i != clicks: #checks if correct square was clicked in the correct order
                           correct = False #if clicks in wrong order
                        clicks += 1
                        if clicks == S:
                            STATE = "feedback"

            if STATE == "summary wait":
                if event.type == MOUSEBUTTONDOWN and event.button == LEFT:
                    clickpos = pygame.mouse.get_pos()
                    if end_button.collidepoint(clickpos):
                        STATE = "goodbye"
                        
            if event.type == KEYDOWN and event.key == K_ESCAPE:
               STATE = "quit"
               break

            if event.type == QUIT:
               STATE = "quit"
               break

        # automatic transitionals       
        if STATE == "welcome":
           start_wait_time = time.time()
           STATE = "welcome wait"

        if STATE == "welcome wait" and time.time() - start_wait_time >= 3:
           STATE = "task introduction"
       
        if STATE == "feedback":
            total_trials += 1
            if correct: #if correct=True
                incorrect_trials = 0 #incorrect_trails are set back to 0, internal variable that runs from 0 - 2
                draw_feedback_correct()
                correct_trials += 1
                S += 1  #one more square shown in sequence if correct
                if S == NUM_SQUARES:
                    STATE = "summary"
            else:
                draw_feedback_incorrect()
                incorrect_trials += 1
                if incorrect_trials == 2:
                    STATE = "summary"
                elif S > 2:
                    S -= 1 #one less square shown in sequence if incorrect
            if STATE == "feedback": #still in state feedback?
                start_wait_time = time.time()
                STATE = "feedback wait"

        if STATE == "feedback wait" and time.time() - start_wait_time >= 2:
           STATE = "new sequence"
           
        if STATE == "new sequence":
           draw_new_sequence()
           STATE = "trial"
           clicks = 0 #clicks are counted
           correct = True #sequence is set to correct=True if wrong correct=False
           
        if STATE == "summary":
           score = calculate_summary() #get calculated score from function
           end_button = draw_summary(score)
           with open('Results_Corsi.txt', 'w') as f: #creates file
               print >> f, 'Correct trials:', correct_trials
               print >> f, 'Incorrect trials:', total_trials - correct_trials
               print >> f, 'Total trials:', total_trials
               print >> f, 'Score:', score
           STATE = "summary wait"
       
        if STATE == "goodbye":
           start_wait_time = time.time()
           STATE = "termination wait"
           
        if STATE == "termination wait" and time.time() - start_wait_time >= 3:
           STATE = "quit"
           
        if STATE == "quit":
           break

        # presentationals
        if STATE == "welcome wait":
           draw_welcome()

        if STATE == "task introduction":
           draw_task_introduction()
           start_button = draw_start_button()

        if STATE == "termination wait":
           draw_goodbye()

        # Updating the display
        pygame.display.update()


#welcome screen
def draw_welcome():
    surface.fill(BACKGR_COL)
    text_surface = myfont.render("Corsi Block Tapping Task", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_WIDTH/2,150)
    screen.blit(text_surface, text_rectangle)
    
# creates and draws start button
def draw_start_button():
    start_button = pygame.draw.rect(surface,(col_gray),(450,500,100,50))
    pygame.display.flip()
    text = myfont.render("Start", True, col_black)
    screen.blit(text, (start_button.centerx - text.get_width()/2, start_button.centery - myfont.get_height() / 2))
    return start_button

#task introduction screen with start button
def draw_task_introduction():
    surface.fill(BACKGR_COL)
    text_surface = myfont.render("Task Introduction", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.height = 100
    text_rectangle.center = (SCREEN_WIDTH/2,150)
    screen.blit(text_surface, text_rectangle)

    text_surface = myfont_small.render("Observe the sequence of blocks that light up yellow and then repeat the sequence back in order.", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_WIDTH/2,300)
    screen.blit(text_surface, text_rectangle)

    text_rectangle.center = (SCREEN_WIDTH/2,350)
    text_surface = myfont_small.render("You have two attempts per level, try to remember the sequence of all 9 blocks. Good luck!", True, col_black, BACKGR_COL)
    screen.blit(text_surface, text_rectangle)

# creates random squares that do not overlap
def add_square():
    while True:
        x = randint(MARGIN, SCREEN_WIDTH - SQUARE_WIDTH - MARGIN)
        y = randint(MARGIN, SCREEN_HEIGHT - SQUARE_WIDTH - MARGIN)
        square = pygame.Rect(x, y, SQUARE_WIDTH, SQUARE_WIDTH)
        bigger_square = square.inflate(MARGIN, MARGIN)
        #print square, bigger_square
        if bigger_square.collidelist(Squares) < 0:
           break
    Squares.append(square)
    return square

#creates numbers for squares when sequance is shown
def draw_rect(R, color = col_black, label = ""):
    pygame.draw.rect(surface, color, R)
    if label != '':
        text = myfont.render(label, True, col_black)
        screen.blit(text, (R.centerx - text.get_width()/2, R.centery - myfont.get_height() / 2))

#creates new sequence of squares
def draw_new_sequence():
    surface.fill(BACKGR_COL)
    global Squares
    Squares = []
    for i in range(0, NUM_SQUARES):
        R = add_square()
        draw_rect(R, col_blue)

    # Updating the display
    pygame.display.update()
    pygame.event.get() # for mac

    # Show sequence (blue squares turn yellow)
    for i in range(0, S):
        R = Squares[i]
        draw_rect(R, color=col_yellow, label=str(i+1))
        pygame.display.update()
        pygame.event.get() # for mac

        #wait for 0.8 seconds
        start_wait_time = time.time()
        while True:
            if time.time() - start_wait_time >= 0.8:
                break

        draw_rect(R, col_blue)
        pygame.display.update()
        pygame.event.get() # for mac

#flashes clicked square yellow and back to blue and returns index of clicked square
def clicked_square_index():
    clickpos = pygame.mouse.get_pos() #gets the clickposition
    for i in range(0, len(Squares)):
        R = Squares[i] #R is one of the squares
        if R.collidepoint(clickpos): #if clickposition collides with a square(R)
            draw_rect(R, col_yellow)
            pygame.display.update()
            while True:
                event = pygame.event.wait()
                if event.type == MOUSEBUTTONUP and event.button == LEFT:
                    break
            draw_rect(R, col_blue)
            pygame.display.update()
            pygame.event.get() # for mac
            return i
    return -1 #if background is clicked

# draw feedback screen if correct
def draw_feedback_correct():
    surface.fill(BACKGR_COL)
    text_surface = myfont.render("Correct!", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_WIDTH/2,150)
    screen.blit(text_surface, text_rectangle)

# draw feedback screen if incorrect
def draw_feedback_incorrect():
    surface.fill(BACKGR_COL)
    text_surface = myfont.render("Incorrect!", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_WIDTH/2,150)
    screen.blit(text_surface, text_rectangle)

#calculates final score
def calculate_summary():
    score = 100*correct_trials/total_trials
    return score

#creates and draws quit button
def draw_end_button():
    end_button = pygame.draw.rect(surface,(col_gray),(450,500,100,50))
    pygame.display.flip()
    text = myfont.render("Quit", True, col_black)
    screen.blit(text, (end_button.centerx - text.get_width()/2, end_button.centery - myfont.get_height() / 2))
    return end_button

#summary screen with score and quit button
def draw_summary(score):
    surface.fill(BACKGR_COL)
    text_surface = myfont.render("Summary", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_WIDTH/2,150)
    screen.blit(text_surface, text_rectangle)

    text_surface = myfont_small.render("Your score is " + str(score) + "%", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_WIDTH/2,300)
    screen.blit(text_surface, text_rectangle)
    return draw_end_button() # returns end button

#goodbye screen
def draw_goodbye():
    surface.fill(BACKGR_COL)
    text_surface = myfont.render("Goodbye!", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_WIDTH/2,150)
    screen.blit(text_surface, text_rectangle)

main()
quit()