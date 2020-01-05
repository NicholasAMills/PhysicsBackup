import pygame
from Vec2 import Vec2
from circle import Circle
import random
import math

ball = Circle()
objects = []
exploded_objects = []
gameSpeed = 1000

# Random values for radius, ball color, velocity, and starting position
def random_ball():
    radius = random.randint(40, 80)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    pos_x = random.randint(80, 720)
    pos_y = 800

    if pos_x <= 213:
        vel_x = random.randint(0, 300)
    elif pos_x >= 426:
        vel_x = random.randint(-300, 0)
    elif pos_x > 213 & pos_x < 426:
        vel_x = random.randint(-300, 300)
    vel_y = -random.randint(400, 800)

    mass = random.randint(1, 2)
    ball = (Circle(radius=radius, color=color, pos=Vec2(pos_x, pos_y), vel=Vec2(vel_x, vel_y), mass=mass))

    return ball


# Gravity value for the object
def gravity(obj):
    g = Vec2(0, 10)
    return obj.mass * g

def main():
    # Set up pygame and window
    pygame.init()
    # Set the screen size for the pygame window
    screen = pygame.display.set_mode(size=[800, 600])
    # Sets the background color of the pygame window to white
    bg_color = [255, 255, 255]
    screen.fill(bg_color)
    score = 0

    # Game Loops
    running = True
    # clock within pygame
    clock = pygame.time.Clock()
    # Sets the fps of the game to 60
    fps = 60
    dt = 1/fps
    # Variable to set game to run in slow motion
    runSlow = False

    # Select the font
    font = pygame.font.SysFont('Calibri', 50, True, False)
    # Variable to hold the color black
    BLACK = [0, 0, 0]

    while running:
        # Adds up to 5 ball object to the array of objects
        if len(objects) < 5:
            objects.append(random_ball())
            print(len(objects))

        # Add forces to the objects (ball)
        for o in objects:
            o.add_force(gravity(o))
            o.update(dt)
            if o.pos.y > 800:
                objects.pop(objects.index(o))

        # Give explosion circles forces
        for e in exploded_objects:
            e.add_force(gravity(e))
            e.update(dt)
            if e.pos.y > 800:
                exploded_objects.pop(exploded_objects.index(e))

        # Display objects to screen
        screen.fill(bg_color)

        # draws normal circles
        for o in objects:
            o.draw(screen)

        # Setting up scoreboard
        text = font.render("Score: " + str(score), True, BLACK)
        # Put the image of the text on the screen at 250x250
        screen.blit(text, [50, 50])

        # Draws explosion dots
        for e in exploded_objects:
            e.draw(screen)

        # Show what we've drawn
        pygame.display.flip()

        # Wait enough so that the frame can keep up
        if runSlow:
            dt = clock.tick(fps)/2000
        else:
            dt = clock.tick(fps)/1000

        # Event loop
        for e in pygame.event.get():

            if e.type == pygame.QUIT:  # user clicked close
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:  # left mouse button
                # If user just clicks a circle and not holds, they get 2 points
                # Storing mouse x and y positions
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                # Checking if mouse is inside a circle
                for o in objects:
                    sqx = (x - o.pos.x)**2
                    sqy = (y - o.pos.y)**2
                    if math.sqrt(sqx + sqy) < o.radius:
                        objects.pop(objects.index(o))
                        i = 0
                        # Draw explosion circles
                        while i < 5:
                            exploded = Circle(radius=random.randint(5, 15), color=(0, 0, 0), pos=Vec2(o.pos.x, o.pos.y),
                                              vel=Vec2(random.randint(-300, 300), random.randint(-300, 300)),
                                              mass=random.randint(1, 2))
                            exploded_objects.append(exploded)
                            i += 1
                        score += 2

            # Hold down mouse 1 and drag to pop circles, but only gives 1 point
            elif pygame.mouse.get_pressed()[0]:
                try:
                    # get mouse position
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]

                    for o in objects:
                        # distance formula to check if mouse is inside a circle
                        sqx = (x - o.pos.x) ** 2
                        sqy = (y - o.pos.y) ** 2
                        if math.sqrt(sqx + sqy) < o.radius:
                            objects.pop(objects.index(o))
                            i = 0
                            while i < 5:
                                exploded = Circle(radius=random.randint(5, 15), color=(0, 0, 0),
                                                  pos=Vec2(o.pos.x, o.pos.y),
                                                  vel=Vec2(random.randint(-300, 300), random.randint(-300, 300)),
                                                  mass=random.randint(1, 2))
                                exploded_objects.append(exploded)
                                i += 1
                            score += 1 # user only gets 1 point for dragging
                except AttributeError:
                    pass
            key = pygame.key.get_pressed()

            # If user presses the spacebar, it will pop all circles on screen but add no score
            if key[pygame.K_SPACE]:
                for o in objects:
                    i = 0
                    while i < 5:
                        # draw black circles as the explosion
                        exploded = Circle(radius=random.randint(5, 15), color=BLACK, pos=Vec2(o.pos.x, o.pos.y),
                                          vel=Vec2(random.randint(-300, 300), random.randint(-300, 300)),
                                          mass=random.randint(1, 2))
                        exploded_objects.append(exploded) # adds explosion circle to list
                        i += 1
                objects.clear() # remove all circles from objects list, hence deleting them from the screen

            # If left shift is held down, runSlow is set to true and the game runs at 1/2 speed
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LSHIFT:
                    runSlow = True
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_LSHIFT:
                    runSlow = False

    # Shut down pygame
    pygame.quit()


# Safe start
if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame().quit()
        raise
