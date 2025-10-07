import pygame, sys
from config import *
from josephus import JosephusVis


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hacker Josephus Visualizer")
    clock = pygame.time.Clock()


    vis = JosephusVis(screen)
    running = True
    while running:
        vis.maybe_auto_step()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not vis.on_click(event):
                    pass

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    vis.auto = not vis.auto
                elif event.key == pygame.K_n:
                    vis.do_step()
                elif event.key == pygame.K_r:
                    vis.reset()
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    vis.set_n(vis.n - 1)
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    vis.set_n(vis.n + 1)

        vis.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()