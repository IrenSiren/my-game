
import sys
import pygame
import math
from math import pi
from math import sqrt
from math import hypot
from math import atan2
from pygame.locals import *
from pygame.draw import *
from random import randint
from random import randrange
pygame.init()

#define screen size
screen_width = 800
screen_hight = 600

FPS = 10
screen = pygame.display.set_mode((screen_width, screen_hight))
myfont = pygame.font.SysFont("monospace", 16)

n=10
size = 40

#density
p = 0.5       

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Background
background = pygame.image.load('space_stars.jpg')

#define colors
RED = (195, 33, 72)
BLUE = (185, 222, 250)
YELLOW = (251, 228, 126)
GREEN = (150, 196, 87)
MAGENTA = (255, 150, 167)
CYAN = (116, 153, 231)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

#draw score
def draw_text(x, y):
  score_txt = font.render("Score : " + str(score), True, (255, 255, 255))
  screen.blit(score_txt, (x, y))


ball_list=[]
for u in range (n):
  r = randrange(20, size)
  m = int(r * pi * p)

  ball = { 'r' : r,
           'x': randint(r+10, screen_width - r),
           'y' : randint(r+10, screen_hight - r),
           'v_x' : randrange(7, 17),
           'v_y' : randrange(7, 17),
           'color' : COLORS[randint(0, 5)],
           'm' : m }
  ball_list.append(ball)


def bounce (i):
    if ball_list[i]['y'] > screen_hight - ball_list[i]['r']:
      ball_list[i]['v_y'] *= -1
      ball_list[i]['y'] = screen_hight - ball_list[i]['r']
    if ball_list[i]['y'] < ball_list[i]['r']:
      ball_list[i]['v_y'] *= -1
      ball_list[i]['y'] = ball_list[i]['r']
    if ball_list[i]['x'] > screen_width - ball_list[i]['r'] :
      ball_list[i]['v_x'] *= -1
      ball_list[i]['x'] = screen_width - ball_list[i]['r']
    if ball_list[i]['x'] < ball_list[i]['r']:
      ball_list[i]['v_x'] *= -1
      ball_list[i]['x'] = ball_list[i]['r']

def collision(i, list):
  for k in range (i + 1 , list):
    x_1 = ball_list[i]['x']
    y_1 = ball_list[i]['y']
    x_2 = ball_list[k]['x']
    y_2 = ball_list[k]['y']
    dx = (x_1 - x_2)
    dy = (y_1 - y_2) 
    v_1x = ball_list[i]['v_x']
    v_2x = ball_list[k]['v_x']
    v_1y = ball_list[i]['v_y']
    v_2y = ball_list[k]['v_y']
    m_1 = ball_list[i]['m']
    m_2 = ball_list[k]['m']
    r_1 = ball_list[i]['r']
    r_2 = ball_list[k]['r']

    angle = atan2(dy, dx)
    distance = int (hypot(dx, dy))
    if distance <= r_1 + r_2:
      v_1x_rotate = v_1x * math.cos(angle) + v_1y * math.sin(angle)
      v_2x_rotate = v_2x * math.cos(angle) + v_2y * math.sin(angle)
      v_1y_rotate = v_1y * math.cos(angle) + v_1x * math.sin(angle)
      v_2y_rotate = v_2y * math.cos(angle) - v_2x * math.sin(angle)
      v_1xr_final = ((m_1 - m_2) * v_1x_rotate + 2*m_2 * v_2x_rotate)/(m_2 + m_1)
      v_2xr_final = ((m_2 - m_1) * v_2x_rotate + 2*m_1 * v_1x_rotate)/(m_2 + m_1)

      v_1x_final = v_1xr_final * math.cos(angle) - v_1y_rotate * math.sin(angle) 
      v_2x_final = v_2xr_final * math.cos(angle) - v_2y_rotate * math.sin(angle) 
      v_1y_final = v_1xr_final * math.sin(angle) + v_1y_rotate * math.cos(angle) 
      v_2y_final = v_2xr_final * math.sin(angle) + v_2y_rotate * math.cos(angle) 

      ball_list[i]['v_x'] = int (v_1x_final)
      ball_list[k]['v_x'] = int (v_2x_final)
      ball_list[i]['v_y'] = int (v_1y_final)
      ball_list[k]['v_y'] = int (v_2y_final)

      x_1_rot = x_1 * math.cos(angle) + y_1 * math.sin(angle)
      y_1_rot = y_1 * math.cos(angle) - x_1 * math.sin(angle)
      x_2_rot = x_2 * math.cos(angle) + y_2 * math.sin(angle)
      y_2_rot = y_2 * math.cos(angle) - x_2 * math.sin(angle)
      cross = r_2 + r_1 - distance
      x_1_rot_fin = x_1_rot + cross//2
      x_2_rot_fin = x_2_rot - cross//2

      x_1_f = x_1_rot_fin * math.cos(angle) - y_1_rot * math.sin(angle)
      y_1_f= y_1_rot * math.cos(angle) + x_1_rot_fin * math.sin(angle)
      x_2_f = x_2_rot_fin * math.cos(angle) - y_2_rot * math.sin(angle)
      y_2_f = y_2_rot * math.cos(angle) + x_2_rot_fin * math.sin(angle)

      ball_list[i]['x'] = int (x_1_f)
      ball_list[i]['y'] = int (y_1_f)
      ball_list[k]['x'] = int (x_2_f)
      ball_list[k]['y'] = int (y_2_f)


def draw_balls():
  for i in range (len(ball_list)):
    # make ball bounce
    bounce (i)
    #make collisions
    collision(i, len(ball_list))
    

    pygame.draw.circle(screen, ball_list[i]['color'], [ball_list[i]['x'], ball_list[i]['y']], ball_list[i]['r'])
    ball_list[i]['x'] += ball_list[i]['v_x']
    ball_list[i]['y'] += ball_list[i]['v_y'] 
    


pygame.display.update()
clock = pygame.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)

    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        finished = True
      if event.type == pygame.MOUSEBUTTONDOWN:
        print('Click!') 
        pos = pygame.mouse.get_pos()   
        x_m = pos[0]
        y_m = pos[1]
        print(pos)

        for i in range(len(ball_list)):
          r = ball_list[i]['r']
          x = ball_list[i]['x']
          y = ball_list[i]['y']
          distance = int (hypot(x - x_m , y - y_m))
          if distance <= r :
            score += 1
            print(score)
            

    scoretext = myfont.render("Score {0}".format(score), 1, (0,0,255))
    screen.blit(scoretext, (5, 10))

    screen.fill(BLACK)
    screen.blit(background, (0, 0))
    draw_text(textX, textY)

  
    draw_balls()
    pygame.display.update()
pygame.quit()