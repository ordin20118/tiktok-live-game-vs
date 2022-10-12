import asyncio
import time

import pygame


FPS = 100
width, height = 700, 400


class Ball:  # using a Sprite would be better
    def __init__(self):
        self.ball = pygame.image.load("game/res/character/knight/png/Idle_1.png")
        self.rect = self.ball.get_rect()
        self.speed = [2, 2]

    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed[1] = -self.speed[1]

    def draw(self, screen):
        screen.blit(self.ball, self.rect)


async def pygame_event_loop(event_queue):
    while True:
        await asyncio.sleep(0)  # allow other tasks to run
        event = pygame.event.poll()
        if event.type != pygame.NOEVENT:
            await event_queue.put(event)


async def animation(screen, ball):
    black = 0, 0, 0

    current_time = 0
    while True:
        last_time, current_time = current_time, time.time()
        await asyncio.sleep(1 / FPS - (current_time - last_time))  # tick
        ball.move()
        screen.fill(black)
        ball.draw(screen)
        pygame.display.flip()



async def handle_events(event_queue, ball):
    while True:
        event = await event_queue.get()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if ball.speed == [0, 0]:
                    ball.speed = [2, 2]
                else:
                    ball.speed = [0, 0]
        else:
            pass
            #print("event", event)
    asyncio.get_event_loop().stop()


def main():
    loop = asyncio.get_event_loop()
    event_queue = asyncio.Queue()

    pygame.init()

    pygame.display.set_caption("pygame+asyncio")
    screen = pygame.display.set_mode((width, height))

    ball = Ball()

    pygame_task = asyncio.ensure_future(pygame_event_loop(event_queue))
    animation_task = asyncio.ensure_future(animation(screen, ball))
    event_task = asyncio.ensure_future(handle_events(event_queue, ball))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        pygame_task.cancel()
        animation_task.cancel()
        event_task.cancel()

    pygame.quit()


if __name__ == "__main__":
    main()