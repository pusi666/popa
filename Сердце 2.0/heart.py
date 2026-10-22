import pygame
import math
import sys

# --- НАСТРОЙКИ ---
WIDTH, HEIGHT = 900, 700
BG_COLOR = (40, 0, 10)
TEXT_COLOR = (255, 255, 255)
FPS = 60

TEXT = "I love you "
FONT_SIZE = 20
POINTS_PER_HEART = 200

NUM_HEARTS = 3
DRAW_SECONDS = 10.0
SHRINK_STEP = 0.20
BASE_SCALE = 0.65

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("I love you heart")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", FONT_SIZE, bold=True)

def heart_point(t):
    x = 16 * math.sin(t) ** 3
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    return x, y

def build_heart_points(n, scale_mul):
    raw = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = heart_point(t)
        raw.append((x, y))

    xs = [p[0] for p in raw]
    ys = [p[1] for p in raw]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    margin = 50
    scale = min((WIDTH - 2 * margin) / (max_x - min_x), (HEIGHT - 2 * margin) / (max_y - min_y)) * BASE_SCALE * scale_mul

    cx, cy = WIDTH / 2, HEIGHT / 2
    result = []
    for x, y in raw:
        px = cx + (x - (min_x + max_x) / 2) * scale
        py = cy - (y - (min_y + max_y) / 2) * scale
        result.append((px, py))
    return result

HEARTS = []
for i in range(NUM_HEARTS):
    HEARTS.append(build_heart_points(POINTS_PER_HEART, 1.0 + SHRINK_STEP * i))

def draw_heart(points, drawn_count, offset):
    limit = min(int(drawn_count), len(points))
    for i in range(limit):
        px, py = points[i]
        ch = TEXT[(i + offset) % len(TEXT)]
        if ch == " ":
            continue
        surf = font.render(ch, True, TEXT_COLOR)
        screen.blit(surf, surf.get_rect(center=(px, py)))

def main():
    total = len(HEARTS[0])
    speed = total / (DRAW_SECONDS * FPS)

    current_heart = 0
    progress = 0.0
    offset = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        for h in range(current_heart):
            draw_heart(HEARTS[h], len(HEARTS[h]), 0)

        if current_heart < NUM_HEARTS:
            progress += speed
            if progress >= total:
                progress = total
                draw_heart(HEARTS[current_heart], total, 0)
                current_heart += 1
                progress = 0.0
                offset = 0
            else:
                offset = int(progress) % len(TEXT)
                draw_heart(HEARTS[current_heart], progress, offset)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()