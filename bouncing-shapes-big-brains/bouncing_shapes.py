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
screen = pygame.display.set_mode(size=[800, 600])
grav = Gravity(objects, Vec2(0, 10))


def main():

    # Set up pygame and window
    pygame.init()
    forces = []
    # Set background color
    bg_color = [255, 255, 255]
    # Set the screen size
    screen.fill(bg_color)

    gravX = 0
    gravY = 0

    drag = False
    objToDrag = None

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

    walls.append(Wall(pos=Vec2(70, 280), normal=Vec2(1, 0), length=230))
    walls.append(Wall(pos=Vec2(730, 280), normal=Vec2(-1, 0), length=230))
    walls.append(Wall(pos=Vec2(400, 60), normal=Vec2(0, 1), length=350))
    walls.append(Wall(pos=Vec2(400, 500), normal=Vec2(0, -1), length=350))

    # Declaring shapes
    # OFFSETS
    red_Offsets = []
    blue_Offsets = [Vec2(-60, 60), Vec2(0, -60), Vec2(60, 60)]
    blue_Offsets.reverse()
    green_Offsets = [Vec2(-25, -25), Vec2(-25, 25), Vec2(25, 25), Vec2(25, -25)]
    purple_Offsets = [Vec2(-60, -30), Vec2(-30, -60), Vec2(60, 30), Vec2(30, 60)]
    purple_Offsets.reverse()
    yellow_Offsets = []
    black_Offsets = []

    for i in range(6):
        x = 50 * math.cos(i * math.pi / 3)
        y = 50 * math.sin(i * math.pi / 3)
        red_Offsets.append(Vec2(x, y))
    red_Offsets.reverse()

    for i in range(360):
        x = math.cos(i * math.pi / 180)
        y = math.sin(i * math.pi / 180)
        black_Offsets.append(Vec2(x, y))
    black_Offsets.reverse()

    for i in range(8):
        x = 70 * math.cos(i * math.pi / 4)
        y = 70 * math.sin(i * math.pi / 4)
        yellow_Offsets.append(Vec2(x, y))
    yellow_Offsets.reverse()

    redOctagon = UniformPolygon(mass=30, pos=Vec2(300, 300), vel=Vec2(0, 0), offsets=red_Offsets, color=RED, width=0)
    blueTriangle = UniformPolygon(mass=40, pos=Vec2(550, 320), vel=Vec2(0, 0), offsets=blue_Offsets, color=BLUE, width=0)
    greenSquare = UniformPolygon(mass=10, pos=Vec2(100, 100), vel=Vec2(0, 0), offsets=green_Offsets, color=GREEN, width=0)
    yellowStar = UniformPolygon(mass=50, pos=Vec2(500, 200), vel=Vec2(0, 0), offsets=yellow_Offsets, color=YELLOW, width=0)
    purpleRectangle = UniformPolygon(mass=20, pos=Vec2(300, 200), vel=Vec2(0, 0), offsets=purple_Offsets, color=PURPLE,
                                     width=0)
    blackCircle = UniformPolygon(mass=float('inf'), pos=Vec2(200, 200), vel=Vec2(0, 0), offsets=black_Offsets, color=BLACK, width=0)

    objects.append(redOctagon)
    objects.append(blueTriangle)
    objects.append(greenSquare)
    objects.append(purpleRectangle)
    objects.append(yellowStar)

    for w in walls:
        objects.append(w)

    # gravity
    grav = Gravity(objects, Vec2(gravX, gravY))
    forces.append(grav)

    while running:
        for o in objects:
            o.clear_force()

        # Add Force
        for f in forces:
            f.apply()

        # Draw objects to screen
        screen.fill(bg_color)

        for o in objects:
            o.update(dt)
            o.draw(screen)

        blackCircle.update(dt)
        # blackCircle.draw(screen)

        for w in walls:
            w.update(dt)
            w.clear_force()
            w.draw(screen)

        # checking collisions
        for a, b in itertools.combinations(objects, 2):
            contact(a, b, restitution=1)

        # Wait
        fps = 60
        clock.tick(fps) / 1000

        # Referencing mouse location
        mousePos = Vec2(pygame.mouse.get_pos())  # storing mouse position into a variable
        mouseX = mousePos.x  # reference for x component
        mouseY = mousePos.y  # reference for y component

        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        point = Vec2(x, y)

        blackCircle.pos = mousePos

        key = pygame.key.get_pressed()  # referencing key event
        # Event Loop

        contactResult = ()

        for e in pygame.event.get():
            # user clicks closed button
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                # blackCircle.pos = point
                for o in objects:
                    contactResult = contact(blackCircle, o, resolve=output)
                    # pointOfContact = contactResult[4]
                    if contactResult is not None:
                        drag = True
                        objToDrag = o

            elif e.type == pygame.MOUSEBUTTONUP and e.button == 3:
                drag = False

            elif e.type == pygame.MOUSEMOTION:
                pass
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                pass

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    if grav.g.x < 1000:
                        grav.g.x += 100
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    if grav.g.x > -1000:
                        grav.g.x -= 100
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    if grav.g.y > -1000:
                        grav.g.y -= 100
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    if grav.g.y < 1000:
                        grav.g.y += 100
        pygame.display.flip()

        if drag:
            objToDrag.vel = Vec2(0, 0)

            # newLocX = (int(objToDrag.pos.x) - mouseX)**2
            # newLocY = (int(objToDrag.pos.y) - mouseY)**2
            # newLoc = math.sqrt(newLocX + newLocY)
            #
            # finalY = math.cos(45) * newLoc
            # finalX = math.sin(45) * newLoc
            # print(finalX, finalY)
            # print(newLoc)
            # objToDrag.pos = Vec2(finalX, finalY)

            objToDrag.pos = mousePos
            objToDrag.avel = 0

    # Shut down pygame
    pygame.quit()


# Safe start
if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise
