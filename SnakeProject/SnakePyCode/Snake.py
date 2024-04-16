import pygame
import random
import sys
import os

def resource_path(relative_path):
    base_path = getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath("Snake.py")))
    return os.path.join(base_path,relative_path)
pygame.init()

white = (255 , 255 , 255)
blue = (0 , 0 , 255)
red = (255 , 0 , 0)
bg_color = (89, 213, 224)
snake_color = (250, 163, 0)
food_color = (244, 83, 138)
inside_food_color = (220, 60, 110)
WIDTH = 800
HEIGHT = 600
dis = pygame.display.set_mode((WIDTH, HEIGHT)) 

game_over_image = pygame.image.load(resource_path("Snake/game_over.jfif")).convert()
monke = pygame.image.load(resource_path("Snake/monke.png")).convert()
face = pygame.image.load(resource_path("Snake/face.png")).convert_alpha()
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))
monke = pygame.transform.scale(monke, (WIDTH, HEIGHT))
face = pygame.transform.scale(face, (40, 28))
monke = monke.convert_alpha()
monke.set_alpha(50)
font = pygame.font.Font('freesansbold.ttf', 32)

text = font.render('GAME OVER', True, blue)
textRect = text.get_rect()
textRect.center = (WIDTH/2, HEIGHT/2)
pygame.display.update()
pygame.display.set_caption("snake hee hee haw haw")

game_over = False
clock = pygame.time.Clock()
snake_speed = 10

def shuffleFood(WIDTH, HEIGHT, snake_block, snakeList):
    foodx = random.randrange(0, WIDTH-snake_block, snake_block)
    foody = random.randrange(snake_block, HEIGHT, snake_block)
    if (foodx, foody) in snakeList:
        return shuffleFood(WIDTH, HEIGHT, snake_block, snakeList)
    else:
        return foodx, foody
def drawSnake(snakeList, snake_block):
    red = snake_color[0]
    green = snake_color[1]
    blue = snake_color[2]
    for block in snakeList:
        pygame.draw.rect(dis, (red,min(green + 2*snakeList.index(block), 255), min(blue + 10*snakeList.index(block), 255)), [block[0], block[1], snake_block, snake_block])
        pygame.draw.rect(dis, snake_color, [block[0] + 5, block[1] + 5, snake_block - 5, snake_block - 5], border_radius=2)
        if snakeList.index(block) == len(snakeList)-1:
            dis.blit(face, (block[0],block[1]+5))
def Loop():
    game_over = False
    game_close = False
    direction_set = False
    x1 = 120
    y1 = 120
    snakeList = []
    snakeLength = 1
    snake_block = 40
    x1_change = 0
    y1_change = 0
    score = 0
    foodx = random.randrange(0, WIDTH-snake_block, snake_block)
    foody = random.randrange(snake_block, HEIGHT, snake_block)
    while game_over == False:
        while game_close == True:
            dis.fill(white)
            dis.blit(game_over_image, (0,0))
            dis.blit(text, textRect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        Loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT) and (x1_change != snake_block) and (direction_set == False):
                    direction_set = True
                    x1_change = -snake_block
                    y1_change = 0
                elif (event.key == pygame.K_RIGHT) and (x1_change != -snake_block) and (direction_set == False):
                    direction_set = True
                    x1_change = snake_block
                    y1_change = 0
                elif (event.key == pygame.K_UP) and (y1_change != snake_block) and (direction_set == False):
                    direction_set = True
                    x1_change = 0
                    y1_change = -snake_block
                elif (event.key == pygame.K_DOWN) and (y1_change != -snake_block) and (direction_set == False):
                    direction_set = True
                    x1_change = 0
                    y1_change = snake_block

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        snakeHead = []
        snakeHead.append(x1)
        snakeHead.append(y1)
        snakeList.append(snakeHead)
        if len(snakeList) > snakeLength:
            del snakeList[0]
        for x in snakeList[:-1]:
            if x == snakeHead:
                game_close = True
        dis.fill(bg_color)
        dis.blit(monke, (0,0))
        drawSnake(snakeList, snake_block)
        pygame.draw.rect(dis, food_color, [foodx, foody, snake_block, snake_block])
        pygame.draw.rect(dis, inside_food_color, [foodx + 5, foody + 5, snake_block - 7.5, snake_block - 7.5], border_radius=2)
        
        for i in range(int(WIDTH / snake_block)):
            pygame.draw.line(dis, (89, 213, 250), (i*snake_block, WIDTH), (i*snake_block, 0))
        for i in range(int(HEIGHT / snake_block)):
            pygame.draw.line(dis, (89, 213, 250), (WIDTH, i*snake_block), (0, i*snake_block))

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            score += 1
            foodx, foody = shuffleFood(WIDTH, HEIGHT, snake_block, snakeList)
            snakeLength += 1
            pygame.display.set_caption("Score: " + str(score))

        direction_set = False
        clock.tick(snake_speed)
    
    pygame.quit()
    return ""
Loop()
