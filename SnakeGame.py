import pygame, sys, random

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRIDSIZE = 20 # size of squares
GRID_WIDTH = SCREEN_HEIGHT / GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH / GRIDSIZE

UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

class SNAKE(object):
    def __init__(self):
        self.length = 1 # initial length and positions of snake
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (15,25,45) # dark blue color for the snake

    def get_head_position(self):
        return self.positions[0] # find first position of snake
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return # do not turn if length > 1 and attempting opposite direction
        else: self.direction = point
    
    def move(self):
        current = self.get_head_position(); x, y = self.direction # current head position and direction
        new = (((current[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), (current[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT)
        
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset() # reset if snake hits itself
        
        if new[0] - current[0] != x*GRIDSIZE or new[1] - current[1] != y*GRIDSIZE:
            self.reset() # reset if snake hits wall
        
        else: # add a new head position
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop() # pop last
            
    def reset(self):
        self.length = 1 # re-initialize snake
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
    
    def draw(self, surface):
        for p in self.positions: # draw snake for each position
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (90, 215, 230), r, 1)
    
    def handle_keys(self):
        for event in pygame.event.get():
            
            # exit both pygame and snake
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                
            # keys to handle the game controls    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
    
class FOOD(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (225, 165, 50)
        self.randomize_position()
    
    def randomize_position(self): # get random position and place food there
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)
    
    def draw(self, surface): # draw food surface
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (90, 215, 230), r, 1)
    
def drawGrid(surface): # game surface
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0: # draw light blue rectangles on the surface
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (90, 215, 230), r)
                
            else: # draw different shade of light blue rectangles on surface
                rr = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (85, 195, 205), rr)

def main():    
    pygame.init()
    
    clock = pygame.time.Clock() # initialize clock and game screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32)
    
    # set the surface and draw the visible grid
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)
    
    # get snake and food objects
    snake = SNAKE(); food = FOOD()
    
    myfont = pygame.font.SysFont("monospace", 16)
    
    score = 0 # initialize score
    
    while True:
        clock.tick((score/2)+10) # square/sec
        snake.handle_keys() # allow direction
        drawGrid(surface) # draw surface
        snake.move() # start movement
        
        # increase length and score if snake eats food
        if snake.get_head_position() == food.position:
            snake.length += 1; score += 1
            food.randomize_position()
        
        # randomize food if lands on snake body
        if food.position in snake.positions[2:]:
            food.randomize_position()
        
        # initialize score
        if snake.length == 1:
            score = 0
        
        # draw new surface
        snake.draw(surface)
        food.draw(surface)
        
        # update and refresh screen
        screen.blit(surface, (0,0))
        pygame.display.update()
        
        # show new score and update
        text = myfont.render("Score {0}".format(score), 1, (0,0,0))
        screen.blit(text, (5,10)); pygame.display.update()
        
if __name__ == "__main__":
    main()