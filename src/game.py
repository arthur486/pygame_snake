"""
Source materials: https://docs.replit.com/tutorials/19-build-snake-with-pygame

Copyright

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from enum import Enum
from random import randint
import pygame


class Direction(Enum):
    """
    Enumerate possible directions in which the snake can travel
    """
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Food:
    """
    Represent one food item for the snake

    ! Python uses indentation instead of { } or begin ... end to delimitate blocks of code, so everything having the
    same indentation is at the same level; in this case, functions __init__, draw and respawn are inside the Food class
    """
    # TODO Replace the green rectangles with a nice drawing, like in https://www.google.com/search?q=snake
    color = (0, 255, 0)
    x = 0
    y = 0
    bounds = None

    def __init__(self, block_size, bounds):
        """
        This is a special method call a 'constructor', which we use to create food items
        """
        self.block_size = block_size
        self.bounds = bounds

    def draw(self, game, window):
        """
        Draw the food item on screen as a green rectangle (see the (0,255,0) above)
        The 'game' variable is created by PyGame and keeps the state of the game, screen and so on...
        """
        game.draw.rect(window, self.color, (self.x, self.y, self.block_size, self.block_size))

    def respawn(self):
        """
        We create a random location for the next food item
        self.x, self.y will hold the position of this (Python's self is like C++/C#/Java's this) food item
        """
        # TODO How can we make sure the food item does not overlap the snake itself?
        blocks_in_x = (self.bounds[0]) / self.block_size;
        blocks_in_y = (self.bounds[1]) / self.block_size;
        self.x = randint(0, blocks_in_x - 1) * self.block_size
        self.y = randint(0, blocks_in_y - 1) * self.block_size


class Snake:
    """
    Represent the snake itself. We have to know the location of all its body segments, current direction and color
    """
    length = None
    direction = None
    body = None
    block_size = None
    # TODO Have the snake be colored and use sprites, like in https://www.google.com/search?q=snake
    color = (0, 0, 255)
    bounds = None

    def __init__(self, block_size, bounds):
        """
        We call this method to create the snake when starting the program
        We need block_size and bounds to figure out the size of the game board
        """
        self.block_size = block_size
        self.bounds = bounds
        self.respawn()

    def respawn(self):
        """
        We call this function to start/restart the game; it sets the snake's initial length (3 blocks), the position of
        each of the 3 body segments (self.body) and the direction its going (Direction.DOWN)
        """
        self.length = 3
        self.body = [(20, 20), (20, 40), (20, 60)]
        self.direction = Direction.DOWN

    def draw(self, game, window):
        """
        We draw the snake by drawing each segment of its body
        """
        for segment in self.body:
            # TODO Draw the snake's head using a different color than its body
            game.draw.rect(window, self.color, (segment[0], segment[1], self.block_size, self.block_size))

    def move(self):
        """
        self.body is the list of the snake's body segments
        self.body[-1] is the last element of the list -> this is where we keep the snake's head
        """
        curr_head = self.body[-1]
        """
        Decide where the snake's head is going to be, based on its direction 
        """
        if self.direction == Direction.DOWN:
            """
            If the snake is heading down, then the head will move on the OY direction towards the bottom of the screen
            There is one case for each possible direction of travel
            """
            next_head = (curr_head[0], curr_head[1] + self.block_size)
            self.body.append(next_head)
        elif self.direction == Direction.UP:
            next_head = (curr_head[0], curr_head[1] - self.block_size)
            self.body.append(next_head)
        elif self.direction == Direction.RIGHT:
            next_head = (curr_head[0] + self.block_size, curr_head[1])
            self.body.append(next_head)
        elif self.direction == Direction.LEFT:
            next_head = (curr_head[0] - self.block_size, curr_head[1])
            self.body.append(next_head)
        """
        We added a new segment for the snake's head when moving it in the code above. So, if the snake did not eat an
        apple, we must remove its last segment. If the snake's head is the last element in the list, then its 'tail' is
        the first element of the list.
        """
        if self.length < len(self.body):
            self.body.pop(0)

    def steer(self, direction):
        """
        Snake can only change direction at a 90 degree angle; so, we disregard trying to go into the opposite direction
        or not changing direction at all
        """
        if self.direction == Direction.DOWN and direction != Direction.UP:
            self.direction = direction
        elif self.direction == Direction.UP and direction != Direction.DOWN:
            self.direction = direction
        elif self.direction == Direction.LEFT and direction != Direction.RIGHT:
            self.direction = direction
        elif self.direction == Direction.RIGHT and direction != Direction.LEFT:
            self.direction = direction

    def eat(self):
        self.length += 1

    def check_for_food(self, food):
        """
        Check if the snake's head (last segment of its body in our representation, remember?) is on top of food; if it
        is, eat it and redraw the snake (+1 to length)
        """
        head = self.body[-1]
        if head[0] == food.x and head[1] == food.y:
            self.eat()
            food.respawn()

    def check_tail_collision(self):
        """
        Check if the snake's head has collided with one of its body segments (except the head, of course); this is a
        game over situation
        """
        head = self.body[-1]
        has_eaten_tail = False

        for i in range(len(self.body) - 1):
            segment = self.body[i]
            if head[0] == segment[0] and head[1] == segment[1]:
                has_eaten_tail = True
        return has_eaten_tail

    def check_bounds(self):
        """
        Check whether the snake's body is within the bounds of the game board. Since we move the snake by adding a new
        segment to its head, it's enough to only check that the head segment is within the board's bounds.
        """
        # TODO Add a nice border to the playing area so that it's obvious the snake should not hit it
        head = self.body[-1]
        if head[0] >= self.bounds[0]:
            return True
        if head[1] >= self.bounds[1]:
            return True

        if head[0] < 0:
            return True
        if head[1] < 0:
            return True
        return False


def start_the_game_already():
    """
    This function is equivalent to C's main() function.
    We use it to initialize the PyGame module, set up the board, create the snake etc...
    """
    pygame.init()
    bounds = (300, 300)
    window = pygame.display.set_mode(bounds)
    pygame.display.set_caption("Snake")

    """
    Size of a game square, in pixels
    """
    block_size = 20
    """
    Create the snake and the first food item placed on the board
    """
    snake = Snake(block_size, bounds)
    # TODO Have more than one food item at any given time on the board
    food = Food(block_size, bounds)
    font = pygame.font.SysFont('comicsans', 60, True)

    """
    Games running in real time will have an event loop, which is a regular loop where the game's events and user input
    are handled.
    """
    run = True
    while run:
        # Delay redrawing everything 100ms
        pygame.time.delay(100)

        """
        PyGame will manage the events for us, we only need to decide what to do for those events that we are interested
        in. We get the next event from the queue using the call pygame.event.get()
        
        In case that event is QUIT we terminate the game
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        """
        Decide where to move the snake depending on which key(s) are pressed; keep in mind that more than one key can
        be pressed at any one time!
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            snake.steer(Direction.LEFT)
        elif keys[pygame.K_RIGHT]:
            snake.steer(Direction.RIGHT)
        elif keys[pygame.K_UP]:
            snake.steer(Direction.UP)
        elif keys[pygame.K_DOWN]:
            snake.steer(Direction.DOWN)

        """
        Actually move the snake
        """
        # TODO Add some sound effects and music to the game :)
        snake.move()
        snake.check_for_food(food)

        if snake.check_bounds() is True or snake.check_tail_collision() is True:
            """
            Check if GAME OVER, wait for 1000ms then restart the game
            """
            text = font.render('Game Over', True, (255, 255, 255))
            window.blit(text, (20, 120))
            pygame.display.update()
            pygame.time.delay(1000)
            snake.respawn()
            food.respawn()

        """
        Update the game window. Not much of a game without this part :)
        """
        window.fill((0, 0, 0))
        snake.draw(pygame, window)
        food.draw(pygame, window)
        pygame.display.update()


"""
This function starts the game. Python programs don't have a main() function, they run by starting a file and interpreting
the source code in it. In our case, the function below is the outermost one indentation-wise, so its the one that the
interpreter runs.
"""
start_the_game_already()
