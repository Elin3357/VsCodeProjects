import pygame
import random
import sys

pygame.init()

CELL_SIZE = 30
GRID_W, GRID_H = 20, 20
SCREEN_W = GRID_W * CELL_SIZE
SCREEN_H = GRID_H * CELL_SIZE + 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (200, 0, 0)
DARK_RED = (150, 0, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (200, 200, 0)
GRAY = (40, 40, 40)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("贪吃蛇")
clock = pygame.time.Clock()
font = pygame.font.SysFont("simhei", 36)
small_font = pygame.font.SysFont("simhei", 24)


def random_food(snake):
    while True:
        pos = (random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))
        if pos not in snake:
            return pos


def draw_cell(pos, color, dark_color):
    x, y = pos[0] * CELL_SIZE, pos[1] * CELL_SIZE + 60
    rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
    pygame.draw.rect(screen, dark_color, rect)
    inner = rect.inflate(-4, -4)
    pygame.draw.rect(screen, color, inner)


def show_game_over(score):
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    t1 = font.render(f"游戏结束  得分: {score}", True, WHITE)
    t2 = small_font.render("按 R 重新开始  按 ESC 退出", True, WHITE)
    screen.blit(t1, (SCREEN_W // 2 - t1.get_width() // 2, SCREEN_H // 2 - 40))
    screen.blit(t2, (SCREEN_W // 2 - t2.get_width() // 2, SCREEN_H // 2 + 10))
    pygame.display.flip()


def main():
    snake = [(GRID_W // 2, GRID_H // 2)]
    dx, dy = 1, 0
    food = random_food(snake)
    score = 0
    game_over = False
    speed = 10
    running = True
    next_dir = (1, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    snake = [(GRID_W // 2, GRID_H // 2)]
                    dx, dy = 1, 0
                    next_dir = (1, 0)
                    food = random_food(snake)
                    score = 0
                    game_over = False
                    speed = 10
                if not game_over:
                    if event.key == pygame.K_UP and dy != 1:
                        next_dir = (0, -1)
                    elif event.key == pygame.K_DOWN and dy != -1:
                        next_dir = (0, 1)
                    elif event.key == pygame.K_LEFT and dx != 1:
                        next_dir = (-1, 0)
                    elif event.key == pygame.K_RIGHT and dx != -1:
                        next_dir = (1, 0)

        if not game_over:
            dx, dy = next_dir
            head = (snake[0][0] + dx, snake[0][1] + dy)
            if (head[0] < 0 or head[0] >= GRID_W or head[1] < 0 or head[1] >= GRID_H or head in snake):
                game_over = True
            else:
                snake.insert(0, head)
                if head == food:
                    score += 1
                    speed = min(speed + 1, 20)
                    food = random_food(snake)
                else:
                    snake.pop()

        screen.fill(BLACK)
        for x in range(GRID_W):
            for y in range(GRID_H):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE + 60, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GRAY, rect, 1)

        for i, seg in enumerate(snake):
            draw_cell(seg, YELLOW if i > 0 else DARK_YELLOW, DARK_YELLOW if i > 0 else YELLOW)

        draw_cell(food, RED, DARK_RED)

        score_text = font.render(f"分数: {score}", True, WHITE)
        screen.blit(score_text, (15, 15))

        if game_over:
            show_game_over(score)

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()
    sys.exit()
    print("hello world")


if __name__ == "__main__":
    main()
