import itertools
import pygame
from Vec2 import Vec2
from Contact import contact
from Contact import point_polygon
import math
from Wall import Wall
from Forces import Gravity
from Polygon import UniformPolygon
from Contact import output

masses = []
objects = []
walls = []
progressSlider = []
screen = pygame.display.set_mode(size=[1500, 800])
grav = Gravity(objects, Vec2(0, 10))


def main():

    # Set up pygame and window
    pygame.init()
    forces = []
    # Set background color
    bg_color = [255, 255, 255]
    # Set the screen size
    screen.fill(bg_color)

    # Game Loops
    running = True
    # clock within pygame
    clock = pygame.time.Clock()
    # Set the fps of the game to 60
    fps = 60
    dt = 1 / fps

    blueTriangleCheck = True

    BLACK = [0, 0, 0]
    RED = [255, 0, 0]
    BLUE = [0, 0, 255]
    YELLOW = [255, 255, 0]
    GREEN = [0, 255, 0]
    PURPLE = [255, 0, 255]

    # BASE
    walls.append(Wall(pos=Vec2(400, 500), normal=Vec2(0, -1), length=500))

    # Declaring shapes
    # OFFSETS
    rocket_tip_offset = [Vec2(0, -30), Vec2(-30, 0), Vec2(30, 0)]
    rocket_tip_offset.reverse()
    purple_Offsets = [Vec2(-20, -40), Vec2(-20, 40), Vec2(20, 40), Vec2(20, -40)]
    purple_Offsets.reverse()

    rocket_tip = UniformPolygon(mass=30, pos=Vec2(300, 159), vel=Vec2(0,0), offsets=rocket_tip_offset, color=RED, width=0)
    purpleRectangle = UniformPolygon(mass=20, pos=Vec2(300, 200), vel=Vec2(0, 0), offsets=purple_Offsets, color=PURPLE, width=0)
    objects.append(rocket_tip)
    objects.append(purpleRectangle)

    for w in walls:
        objects.append(w)

    # gravity
    grav = Gravity(objects, Vec2(0, 1000))
    # forces.append(grav)

    font = pygame.font.SysFont('Calibri', 20, True, False)
    thrustText = font.render("THRUST", True, BLACK)
    fuelText = font.render("FUEL", True, BLACK)

    thrust = False


    while running:
        for o in objects:
            o.clear_force()

        # Add Force
        for f in forces:
            f.apply()

        # Draw objects to screen
        screen.fill(bg_color)

        # Creates Progress Slider on the side of the screen and adds it into a list to be drawn
        pygame.draw.line(screen, BLACK, Vec2(100, 40), Vec2(100, 700), 3)
        pygame.draw.line(screen, BLACK, Vec2(50, 220), Vec2(150, 220), 3)
        pygame.draw.line(screen, BLACK, Vec2(50, 440), Vec2(150, 440), 3)
        pygame.draw.circle(screen, (200, 200, 200), Vec2(100, 40), 20, 0)
        pygame.draw.circle(screen, GREEN, Vec2(100, 700), 80, 0)

        # Creates Thrust and Fuel Bars on top right of screen
        screen.blit(thrustText, [1200, 20])
        screen.blit(fuelText, [1200, 60])
        pygame.draw.rect(screen, BLACK, (1280, 20, 200, 20), 3)
        pygame.draw.rect(screen, BLACK, (1280, 60, 200, 20), 3)
        while thrust:
            pygame.draw.rect(screen, YELLOW, (1280, 20, 197, 17), 0)


        for s in progressSlider:
            s.draw(screen)

        for o in objects:
            o.update(dt)
            o.draw(screen)

        # checking collisions
        for a, b in itertools.combinations(objects, 2):
            contact(a, b, restitution=1)

        # Wait
        fps = 60
        clock.tick(fps) / 1000

        key = pygame.key.get_pressed()  # referencing key event
        # Event Loop

        contactResult = ()

        for e in pygame.event.get():
            # user clicks closed button
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    pass
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    pass

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    thrust = True
                    print("Thrusting")
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_UP:
                    thrust = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    pass

        pygame.display.flip()


    # Shut down pygame
    pygame.quit()


# Safe start
if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise
