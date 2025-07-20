#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import pygame
import sys

# 初始化pygame
pygame.init()

# 游戏窗口尺寸
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 成语列表
IDIOMS = [
    "画蛇添足", "亡羊补牢", "对牛弹琴", "狐假虎威", "井底之蛙",
    "守株待兔", "掩耳盗铃", "自相矛盾", "指鹿为马", "刻舟求剑"
]

# 随机选一个成语  成与语的长度相同
idiom = random.choice(IDIOMS)

# 游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇成语版")
# 尝试加载支持中文的字体
def get_zh_font(size):
    for font_name in ["SimHei", "Microsoft YaHei", "msyh.ttc", "simsun.ttc", "Arial Unicode MS"]:
        try:
            return pygame.font.SysFont(font_name, size)
        except:
            continue
    return pygame.font.SysFont(None, size)
font = get_zh_font(36)

# 蛇和食物
snake = [(5, 5)]
direction = (1, 0)
food = (random.randint(0, (WIDTH // CELL_SIZE) - 1), random.randint(0, (HEIGHT // CELL_SIZE) - 1))
idiom_index = 0
score = 0

def draw_snake(snake):
    for s in snake:
        center = (s[0]*CELL_SIZE + CELL_SIZE//2, s[1]*CELL_SIZE + CELL_SIZE//2)
        radius = CELL_SIZE//2
        pygame.draw.circle(screen, YELLOW, center, radius)

def draw_food(food, char):
    pygame.draw.rect(screen, RED, (food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    text = font.render(char, True, WHITE)
    screen.blit(text, (food[0]*CELL_SIZE, food[1]*CELL_SIZE))

def move_snake(snake, direction):
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    return [head] + snake[:-1]

def check_collision(snake):
    head = snake[0]
    if head[0] < 0 or head[0] >= WIDTH // CELL_SIZE or head[1] < 0 or head[1] >= HEIGHT // CELL_SIZE:
        return True
    if head in snake[1:]:
        return True
    return False

def main():
    global direction, food, idiom_index, score, idiom
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)


        # 判断是否撞墙
        next_x = snake[0][0] + direction[0]
        next_y = snake[0][1] + direction[1]
        hit_wall = (
            next_x < 0 or next_x >= WIDTH // CELL_SIZE or
            next_y < 0 or next_y >= HEIGHT // CELL_SIZE
        )
        if hit_wall:
            # 撞墙时不移动
            pass
        else:
            new_head = (next_x, next_y)
            if new_head == food:
                snake.insert(0, new_head)
                idiom_index += 1
                score += 1
                if idiom_index >= len(idiom):
                    idiom_index = 0
                    # 新成语
                    idiom = random.choice(IDIOMS)
                # 新食物
                while True:
                    food = (random.randint(0, (WIDTH // CELL_SIZE) - 1), random.randint(0, (HEIGHT // CELL_SIZE) - 1))
                    if food not in snake:
                        break
            else:
                snake.insert(0, new_head)
                snake.pop()
            # 撞到自己才会死
            if snake[0] in snake[1:]:
                running = False

        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food, idiom[idiom_index])
        score_text = font.render(f"分数: {score}", True, BLUE)
        idiom_text = font.render(f"成语: {idiom}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(idiom_text, (10, 40))
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
