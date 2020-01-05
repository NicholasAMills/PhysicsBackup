import itertools
import pygame
import pygame.gfxdraw
from circle import Circle
from Vec2 import Vec2
from Contact import contact
from Forces import AttractiveForce
import math
import random
from Polygon import Polygon
from Contact import polygon_polygon
from Contact import output


objects = []

screen = pygame.display.set_mode(size=[800, 600])

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

    randX = random.randrange(50, 100)
    randY = random.randrange(50, 100)
    blueTrianglePos = Vec2(0, 0)

    while running:
        for f in forces:
            f.clear_force()

        # Add Force
        for f in forces:
            f.apply()

        # Draw objects to screen
        screen.fill(bg_color)

        # Wait
        fps = 60
        clock.tick(fps) / 1000

        # Referencing mouse location
        mousePos = Vec2(pygame.mouse.get_pos()) # storing mouse position into a variable
        x = mousePos.x  # reference for x component
        y = mousePos.y  # reference for y component

        # OFFSETS
        red_Offsets = [Vec2(0, -40), Vec2(-40, 40), Vec2(40, 40)]
        blue_Offsets = [Vec2(0, -randY), Vec2(-randX, randY), Vec2(randX, randY)]


        # Drawing blue triangle
        if blueTriangleCheck:  # stops triangle from moving every frame
            randX = random.randrange(50, 100)
            randY = random.randrange(50, 100)
            blueCenterX = random.randrange(100, 700)  # random x value
            blueCenterY = random.randrange(100, 450)  # random y value
            blueTriangleCheck = False  # turning check to false
            blueTrianglePos = Vec2(blueCenterX, blueCenterY)

        # (self,           mass,             pos,       vel,       offsets, color, width):
        redTriangle = Polygon(float('inf'), mousePos, Vec2(0, 0), red_Offsets, RED, 1)
        blueTriangle = Polygon(1, blueTrianglePos, Vec2(0, 0), blue_Offsets, BLUE, 1)

        contact(redTriangle, blueTriangle, resolve=output)
        contactResult = contact(redTriangle, blueTriangle, resolve=output)

        key = pygame.key.get_pressed() # referencing key event
        # Event Loop
        for e in pygame.event.get():
            # user clicks closed button
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:  # left mouse button
                contact(redTriangle, blueTriangle)
                blueTriangle.update_points_normals()
            elif key[pygame.K_SPACE]:
                blueTriangleCheck = True  # setting check back to True to move blue triangle in a new position
                pygame.mouse.set_pos(400, 300)  # putting mouse cursor to the center of the screen

        if contactResult is not None:
            screen.fill(YELLOW)  # YELLOW
            pygame.draw.circle(screen, BLACK, contactResult[4], 5, 0)
            line = contactResult[4] + (contactResult[2] * contactResult[3])
            pygame.draw.line(screen, BLACK, contactResult[4], line, 1)
        else:
            screen.fill(bg_color)

        if redTriangle.pos.x < blueTriangle.pos.x:
            newBlueTrianglePosX = int(math.ceil(blueTriangle.pos.x))
            newBlueTrianglePosY = int(math.ceil(blueTriangle.pos.y))
            print("red is less")

        elif redTriangle.pos.x > blueTriangle.pos.x:
            newBlueTrianglePosX = int(math.floor(blueTriangle.pos.x))
            newBlueTrianglePosY = int(math.ceil(blueTriangle.pos.y))
            print("red is more")


        blueTrianglePos = Vec2(newBlueTrianglePosX, newBlueTrianglePosY)
        redTriangle.draw(screen)
        blueTriangle.draw(screen)

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
