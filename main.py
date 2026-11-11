import random
import sys

import pygame


WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 6
ENEMY_SPEED = 3

BG = (16, 22, 38)
WHITE = (240, 245, 255)
BLUE = (70, 170, 255)
RED = (245, 86, 95)
YELLOW = (255, 205, 70)


def new_enemy():
    size = random.randint(24, 48)
    return pygame.Rect(random.randint(0, WIDTH - size), -size, size, size)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dodge Battle")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)

    player = pygame.Rect(WIDTH // 2 - 22, HEIGHT - 75, 44, 44)
    enemies = [new_enemy() for _ in range(5)]
    score = 0
    game_over = False
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif game_over and event.key == pygame.K_SPACE:
                    player.x, player.y = WIDTH // 2 - 22, HEIGHT - 75
                    enemies = [new_enemy() for _ in range(5)]
                    score = 0
                    game_over = False

        keys = pygame.key.get_pressed()
        if not game_over:
            dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
            dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
            player.x += dx * PLAYER_SPEED
            player.y += dy * PLAYER_SPEED
            player.clamp_ip(screen.get_rect())

            for enemy in enemies:
                enemy.y += ENEMY_SPEED + score // 10
                if enemy.top > HEIGHT:
                    enemies[enemies.index(enemy)] = new_enemy()
                    score += 1
                elif enemy.colliderect(player):
                    game_over = True

        screen.fill(BG)
        # Subtle starfield
        for x in range(20, WIDTH, 80):
            pygame.draw.circle(screen, (34, 44, 66), (x, (x * 7 + pygame.time.get_ticks() // 30) % HEIGHT), 2)
        pygame.draw.rect(screen, BLUE, player, border_radius=9)
        pygame.draw.rect(screen, WHITE, player, 2, border_radius=9)
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy, border_radius=7)
        screen.blit(font.render("DODGE BATTLE", True, WHITE), (20, 18))
        screen.blit(font.render("Score: " + str(score), True, YELLOW), (WIDTH - 145, 18))

        if game_over:
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((5, 8, 18, 190))
            screen.blit(shade, (0, 0))
            title = big_font.render("GAME OVER", True, WHITE)
            prompt = font.render("Press SPACE to try again  |  ESC to quit", True, YELLOW)
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
            screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25)))

        pygame.display.flip()

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
