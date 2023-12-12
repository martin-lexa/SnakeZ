import contextlib

with contextlib.redirect_stdout(None):
    import pygame
# import pygame
import random

# pyinstaller --onefile --noconsole snakes.py

PLAY_FIELD = 600  # Playfield is a square, measurement is also the width of the app window; standard value = 600
WINDOW_HEIGHT = 800
TILE_SIZE = 20  # size of "objects" (single snake body part, apple) --> also "step" size for movement


class Snake:
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_direction = 0
        self.y_direction = 0
        self.length = 1
        self.position_memory = []

    def update_coordinates(self):
        self.x_coord = self.x_coord + TILE_SIZE * self.x_direction
        # checks to see if snake goes out of bounds; if so, places it on the opposite side of the PLAY_FIELD
        if self.x_coord == PLAY_FIELD:
            self.x_coord = 0
        if self.x_coord < 0:
            self.x_coord = PLAY_FIELD - TILE_SIZE
        self.y_coord = self.y_coord + TILE_SIZE * self.y_direction
        if self.y_coord == PLAY_FIELD:
            self.y_coord = 0
        if self.y_coord < 0:
            self.y_coord = PLAY_FIELD - TILE_SIZE
        return None


def get_apple_coordinates(snake1_positions, snake2_posititons):
    apple_x_coord = random.randrange(0, PLAY_FIELD - TILE_SIZE, TILE_SIZE)
    apple_y_coord = random.randrange(0, PLAY_FIELD - TILE_SIZE, TILE_SIZE)
    if (apple_x_coord, apple_y_coord) in snake1_positions or (
        apple_x_coord,
        apple_y_coord,
    ) in snake2_posititons:
        return get_apple_coordinates(snake1_positions, snake2_posititons)
    return (apple_x_coord, apple_y_coord)


def main():

    pygame.init()

    snake1 = Snake(0, 0)
    snake2 = Snake(PLAY_FIELD - TILE_SIZE, PLAY_FIELD - TILE_SIZE)

    apple_eaten = False
    apple_x_coord = random.randrange(0, PLAY_FIELD - TILE_SIZE, TILE_SIZE)
    apple_y_coord = random.randrange(0, PLAY_FIELD - TILE_SIZE, TILE_SIZE)

    pygame.display.set_caption("2 Player Snake")

    window = pygame.display.set_mode((PLAY_FIELD, WINDOW_HEIGHT))
    font = pygame.font.SysFont("arial", 32)

    # define a variable to control the main loop
    running = True

    # main loop
    while running:
        pygame.time.delay(100)  # game speed

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Snake1 movement
                if event.key == pygame.K_a:  # left
                    if not (snake1.x_direction == 1):
                        snake1.x_direction = -1
                        snake1.y_direction = 0
                if event.key == pygame.K_d:  # right
                    if not (snake1.x_direction == -1):
                        snake1.x_direction = 1
                        snake1.y_direction = 0
                if event.key == pygame.K_w:  # up
                    if not (snake1.y_direction == 1):
                        snake1.x_direction = 0
                        snake1.y_direction = -1
                if event.key == pygame.K_s:  # down
                    if not (snake1.y_direction == -1):
                        snake1.x_direction = 0
                        snake1.y_direction = 1

                # Snake2 movement
                if event.key == pygame.K_LEFT:
                    if not (snake2.x_direction == 1):
                        snake2.x_direction = -1
                        snake2.y_direction = 0
                if event.key == pygame.K_RIGHT:
                    if not (snake2.x_direction == -1):
                        snake2.x_direction = 1
                        snake2.y_direction = 0
                if event.key == pygame.K_UP:
                    if not (snake2.y_direction == 1):
                        snake2.x_direction = 0
                        snake2.y_direction = -1
                if event.key == pygame.K_DOWN:
                    if not (snake2.y_direction == -1):
                        snake2.x_direction = 0
                        snake2.y_direction = 1

        """First implementaion of movement/direction changes, 
        seems to get updated less often or whatever
        often misses quick key pushes
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if not (S1_x_direction == 1):
                S1_x_direction = -1
                S1_y_direction = 0
            
        if keys[pygame.K_RIGHT]:
            if not (S1_x_direction == -1):
                S1_x_direction = 1
                S1_y_direction = 0
            
        if keys[pygame.K_UP]:
            if not (S1_y_direction == 1):
                S1_x_direction = 0
                S1_y_direction = -1
            
        if keys[pygame.K_DOWN]:
            if not (S1_y_direction == -1):
                S1_x_direction = 0
                S1_y_direction = 1"""

        # Drawing a Background
        window.fill((100, 100, 100), (0, 0, PLAY_FIELD, PLAY_FIELD))

        # Drawing an apple
        if apple_eaten:
            apple_x_coord, apple_y_coord = get_apple_coordinates(
                snake1.position_memory, snake2.position_memory
            )
            apple_eaten = False
        pygame.draw.rect(
            window, "green", (apple_x_coord, apple_y_coord, TILE_SIZE, TILE_SIZE)
        )

        # Eating Apple
        if apple_x_coord == snake1.x_coord and apple_y_coord == snake1.y_coord:
            apple_eaten = True
            snake1.length += 1
            snake1.position_memory.insert(0, (snake1.x_coord, snake1.y_coord))

        elif apple_x_coord == snake2.x_coord and apple_y_coord == snake2.y_coord:
            apple_eaten = True
            snake2.length += 1
            snake2.position_memory.insert(0, (snake2.x_coord, snake2.y_coord))

        # Drawing snake parts, check if dead, memorizing positions
        snake1.update_coordinates()
        if (snake1.x_coord, snake1.y_coord) in snake1.position_memory or (
            snake1.x_coord,
            snake1.y_coord,
        ) in snake2.position_memory:  # checks if hitting own body
            text = font.render("Snek 1 is ded", True, "green", "blue")
            textRect = text.get_rect()
            textRect.center = (PLAY_FIELD // 2, PLAY_FIELD // 2)
            window.blit(text, textRect)
            pygame.display.update()
            pygame.time.delay(3000)
            running = False
        snake1.position_memory.insert(0, (snake1.x_coord, snake1.y_coord))
        for body_part in range(snake1.length):
            memorized_s1_x, memorized_s1_y = snake1.position_memory[body_part]
            pygame.draw.rect(
                window, "red", (memorized_s1_x, memorized_s1_y, TILE_SIZE, TILE_SIZE)
            )
        snake1.position_memory.pop()

        snake2.update_coordinates()
        if (snake2.x_coord, snake2.y_coord) in snake2.position_memory or (
            snake2.x_coord,
            snake2.y_coord,
        ) in snake1.position_memory:  # checks if hitting own body
            text = font.render("Snek 2 is ded", True, "blue", "green")
            textRect = text.get_rect()
            textRect.center = (PLAY_FIELD // 2, PLAY_FIELD // 2)
            window.blit(text, textRect)
            pygame.display.update()
            pygame.time.delay(3000)
            running = False
        snake2.position_memory.insert(0, (snake2.x_coord, snake2.y_coord))
        for body_part in range(snake2.length):
            memorized_s2_x, memorized_s2_y = snake2.position_memory[body_part]
            pygame.draw.rect(
                window, "blue", (memorized_s2_x, memorized_s2_y, TILE_SIZE, TILE_SIZE)
            )
        snake2.position_memory.pop()

        pygame.display.update()


if __name__ == "__main__":
    main()
