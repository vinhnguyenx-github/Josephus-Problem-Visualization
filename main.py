import asyncio, pygame, sys
from config import *
from josephus import JosephusVis


async def main():
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
                vis.on_click(event)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    vis.auto = not vis.auto
                elif event.key == pygame.K_n:
                    vis.do_step()
                elif event.key == pygame.K_r:
                    vis.reset()
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    vis.set_n(vis.n - 1)
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                    vis.set_n(vis.n + 1)

        vis.draw()
        pygame.display.flip()
        clock.tick(FPS)

        # Sleep a tiny bit to yield control to browser event loop
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # pygbag needs asyncio entrypoint
    asyncio.run(main())