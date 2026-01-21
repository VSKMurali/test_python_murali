import pygame
import sys
import math


def maxwell_color_wheel_simulation():
    pygame.init()
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maxwell's Color Wheel Experiment")
    clock = pygame.time.Clock()

    # Colors (RGB)
    colors = [
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (255, 255, 255)  # White
    ]

    # Sector proportions (can be adjusted like Maxwell did)
    proportions = [0.33, 0.33, 0.33, 0.01]  # Red, Green, Blue, White
    radius = 200
    center = (width // 2, height // 2)

    angle = 0
    rotation_speed = 0.05
    running = True

    font = pygame.font.SysFont(None, 24)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rotation_speed += 0.01
                elif event.key == pygame.K_DOWN:
                    rotation_speed -= 0.01
                elif event.key == pygame.K_r:
                    proportions[0] = min(1.0, proportions[0] + 0.05)
                elif event.key == pygame.K_g:
                    proportions[1] = min(1.0, proportions[1] + 0.05)
                elif event.key == pygame.K_b:
                    proportions[2] = min(1.0, proportions[2] + 0.05)

        screen.fill((30, 30, 30))

        # Draw color wheel sectors
        start_angle = angle
        for i, (color, proportion) in enumerate(zip(colors, proportions)):
            sector_angle = proportion * 2 * math.pi
            end_angle = start_angle + sector_angle

            # Draw sector
            points = [center]
            for a in [start_angle, end_angle]:
                x = center[0] + radius * math.cos(a)
                y = center[1] + radius * math.sin(a)
                points.append((x, y))

            pygame.draw.polygon(screen, color, points)
            start_angle = end_angle

        # Calculate resulting mixed color (average based on proportions)
        total = sum(proportions[:-1])  # Exclude white
        if total > 0:
            mixed_r = sum(colors[i][0] * proportions[i] for i in range(3)) / total
            mixed_g = sum(colors[i][1] * proportions[i] for i in range(3)) / total
            mixed_b = sum(colors[i][2] * proportions[i] for i in range(3)) / total
            mixed_color = (int(mixed_r), int(mixed_g), int(mixed_b))
        else:
            mixed_color = (0, 0, 0)

        # Draw mixed color preview
        mixed_rect = pygame.Rect(center[0] - 50, center[1] - 50, 100, 100)
        pygame.draw.rect(screen, mixed_color, mixed_rect)
        pygame.draw.rect(screen, (200, 200, 200), mixed_rect, 2)

        # Draw info text
        texts = [
            f"Maxwell's Color Wheel Experiment",
            f"Speed: {rotation_speed:.2f} rad/frame (UP/DOWN to adjust)",
            f"Proportions - R: {proportions[0]:.2f} (R key), G: {proportions[1]:.2f} (G key), B: {proportions[2]:.2f} (B key)",
            f"Mixed Color: RGB{mixed_color}",
            f"",
            f"Observations:",
            f"- Adjust proportions to match colors",
            f"- At high speed, colors blend visually",
            f"- R+G = Yellow, G+B = Cyan, R+B = Magenta",
            f"- R+G+B = White (when balanced)"
        ]

        for i, text in enumerate(texts):
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (20, 20 + i * 25))

        # Update angle for rotation
        angle += rotation_speed
        if angle > 2 * math.pi:
            angle -= 2 * math.pi

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    maxwell_color_wheel_simulation()