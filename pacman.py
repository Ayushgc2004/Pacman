import pygame 
import math
import boards as b
pygame.init()

width = 900 
height = 950
screen = pygame.display.set_mode([width,height]) 
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf',20)
level = b.board
color = 'blue'
print("hello world")
color2 = 'red'
run = True
PI = math.pi
def draw_board(lvl):
    num1 = ((height -50)// 32)
    num2 = (width//30)
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen,'white',(j*num2 + (0.5*num2),i*num1 + (0.5*num1)),2)
            if level[i][j] == 2:
                pygame.draw.circle(screen,'white',(j*num2 + (0.5*num2),i*num1 + (0.5*num1)),6)
            if level[i][j] ==3 and j>=15:
                pygame.draw.line(screen,'blue',(j*num2 + (0.5*num2),i*num1),
                                (j*num2 + (0.5*num2),i*num1 + num1),3)
            if level[i][j] == 4 and j>=15:
                pygame.draw.line(screen,'blue',(j*num2,i*num1 + (0.5*num1)),
                                (j*num2+ num2,i*num1 + (0.5*num1)),3)
            if level[i][j] == 9:
                pygame.draw.line(screen,'white',(j*num2,i*num1 + (0.5*num1)),
                                (j*num2+ num2,i*num1 + (0.5*num1)),3)
            if level[i][j] == 5 and j>=15:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6 and j>=15:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7 and j>=15:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8 and j>=15:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] ==3 and j<15:
                pygame.draw.line(screen,color2,(j*num2 + (0.5*num2),i*num1),
                                (j*num2 + (0.5*num2),i*num1 + num1),3)
            if level[i][j] == 4 and j<15:
                pygame.draw.line(screen,color2,(j*num2,i*num1 + (0.5*num1)),
                                (j*num2+ num2,i*num1 + (0.5*num1)),3)
            if level[i][j] == 5 and j<15:
                pygame.draw.arc(screen, color2, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6 and j<15:
                pygame.draw.arc(screen, color2,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7 and j<15:
                pygame.draw.arc(screen, color2, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8 and j<15:
                pygame.draw.arc(screen, color2,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
while run:
    timer.tick(fps)
    screen.fill('black')
    draw_board(level)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()
