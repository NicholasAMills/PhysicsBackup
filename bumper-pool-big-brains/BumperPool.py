import itertools

import pygame
from circle import Circle
from Vec2 import Vec2
from Wall import Wall
from Forces import Friction
from Contact import contact
from Contact import hole_resolve
from Forces import AttractiveForce
import math

walls = []  # wall list
bumpers = []  # bumpers list
redBalls = []  # list of red balls
blueBalls = []  # list of blue balls
balls = []
holes = []
redHoleAr = []
blueHoleAr = []
objects = []
attractives = []
d = 80

screen = pygame.display.set_mode(size=[800, 600])

def main():
    # Balls
    y = 100  # starting position
    blueBallsCheck = []
    redBallsCheck = []

    for i in range(5):
        if (i != 2):
            # Red balls on left side
            redBalls.append(Circle(radius=15, color=(250, 0, 0), pos=Vec2(100, y), mass=1))  # list for keeping track of red balls in play
            # Blue balls on right side
            blueBalls.append(Circle(radius=15, color=(0, 0, 255), pos=Vec2(700, y), mass=1))  # list for keeping track of blue balls in play
        else:
            # Adding top bumpers next to goals
            bumpers.append(Circle(radius=10, color=(0, 255, 0), pos=Vec2(100, y), mass=math.inf))  # Red
            bumpers.append(Circle(radius=10, color=(0, 255, 0), pos=Vec2(700, y), mass=math.inf))  # Blue

            y += 60  # Spacing for bumper
            # Red
            redHole = Circle(radius=20, color=(0, 0, 0), pos=Vec2(100, y), mass=math.inf)
            redHoleAr.append(redHole)  # Red hole position
            redBalls.append(Circle(radius=15, color=(250, 0, 0), pos=Vec2(150, y), mass=1))  # Adding the offset ball to the list
            # Blue
            blueHole = Circle(radius=20, color=(0, 0, 0), pos=Vec2(700, y), mass=math.inf)
            blueHoleAr.append(blueHole)  # Blue goal position
            blueBalls.append(Circle(radius=15, color=(0, 0, 255), pos=Vec2(650, y), mass=1))  # Adding the offset ball to the list

            # Adding bottom bumpers underneath goals
            y += 60  # spacing for bumper
            bumpers.append(Circle(radius=10, color=(0, 255, 0), pos=Vec2(100, y), mass=math.inf))  # Red
            bumpers.append(Circle(radius=10, color=(0, 255, 0), pos=Vec2(700, y), mass=math.inf))  # Blue

        y += 60  # ball spacing

    # Center bumpers
    bumpers.append(Circle(radius=10, color=(0, 255, 0), pos=Vec2(350, 280), mass=math.inf))
    bumpers.append(Circle(radius=10, color=(0, 255, 0), pos=Vec2(300, 280), mass=math.inf))

    bumpers.append(Circle(radius=10, color=(0, 255, 0), pos=Vec2(400, 220), mass=math.inf))
    bumpers.append(Circle(radius=10, color=(0, 255, 0), pos=Vec2(400, 170), mass=math.inf))

    bumpers.append(Circle(radius=10, color=(0, 255, 0), pos=Vec2(450, 280), mass=math.inf))
    bumpers.append(Circle(radius=10, color=(0, 255, 0), pos=Vec2(500, 280), mass=math.inf))

    bumpers.append(Circle(radius=10, color=(0, 255, 0), pos=Vec2(400, 330), mass=math.inf))
    bumpers.append(Circle(radius=10, color=(0, 255, 0), pos=Vec2(400, 380), mass=math.inf))

    # Walls
    walls.append(Wall(pos=Vec2(70, 280), normal=Vec2(1, 0), length=230))
    walls.append(Wall(pos=Vec2(730, 280), normal=Vec2(-1, 0), length=230))
    walls.append(Wall(pos=Vec2(400, 60), normal=Vec2(0, 1), length=350))
    walls.append(Wall(pos=Vec2(400, 500), normal=Vec2(0, -1), length=350))

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

    player = True  # Player 1 and player 2. True = player 1, False = player 2
    canPlay = True
    clickAndDrag = False
    selectedBall = None

    holes = redHoleAr + blueHoleAr

    friction2 = Friction(redBalls)
    forces.append(friction2)

    friction3 = Friction(blueBalls)
    forces.append(friction3)

    font = pygame.font.SysFont('Calibri', 30, True, False)
    BLACK = [0, 0, 0]

    turn = ""
    changeTurn = 0
    redTurn = False
    blueTurn = False
    hasShot = False
    switchPlayer = False

    for r in redBalls:
        objects.append(r)
        redBallsCheck.append(r)
    for b in blueBalls:
        objects.append(b)
        blueBallsCheck.append(b)
    for b in bumpers:
       objects.append(b)
    for w in walls:
       objects.append(w)

    balls = redBalls + blueBalls


    while running:
        # redBallsCheck = redBalls
        # blueBallsCheck = blueBalls

        for r in redBalls:
            r.clear_force()

        for b in blueBalls:
            b.clear_force()

        for a, b in itertools.combinations(objects, 2):
            contact(a, b, restitution=0.65)

        for r in redBalls:
            for h in holes:
                if redBallsCheck == redBalls:
                    contact(r, h, resolve=hole_resolve, list=redBalls)#, list2=redBallsCheck)
                else:
                    #selectedBall = None
                    canPlay = True
                    switchPlayer = False
            #print(r)

        for b in blueBalls:
            for h in holes:
                if blueBallsCheck == blueBalls:
                    contact(b, h, resolve=hole_resolve, list=blueBalls)#, list2=blueBallsCheck)

                else:
                    #selectedBall = None
                    canPlay = True
                    switchPlayer = False

        # Add Force
        for f in forces:
            f.apply()

        for r in redBalls:
            r.update(dt)

        for b in blueBalls:
            b.update(dt)

        # Draw objects to screen
        screen.fill(bg_color)

        for bl in blueHoleAr:
            bl.update(dt)
            bl.clear_force()
            bl.draw(screen)

        for rd in redHoleAr:
            rd.update(dt)
            rd.clear_force()
            rd.draw(screen)

        for r in redBalls:
            r.draw(screen)

        for b in blueBalls:
            b.draw(screen)

        for w in walls:
            w.update(dt)
            w.clear_force()
            w.draw(screen)

        for b in bumpers:
            b.update(dt)
            b.clear_force()
            b.draw(screen)

        # Wait
        fps = 60
        clock.tick(fps) / 1000

        if len(redBalls) == 0:
            # Put the image of the text on the screen at 250x250
            text2 = font.render("Red Wins", True, BLACK)
            screen.blit(text2, [600, 30])
        elif len(blueBalls) == 0:
            # Put the image of the text on the screen at 250x250
            text2 = font.render("Blue Wins", True, BLACK)
            screen.blit(text2, [595, 30])

        if changeTurn % 2 == 0:
            turn = "Red Turn"
            redTurn = True
            blueTurn = False
        elif changeTurn % 2 == 1:
            turn = "Blue Turn"
            blueTurn = True
            redTurn = False

        text = font.render(turn, True, BLACK)
        # Put the image of the text on the screen at 250x250
        screen.blit(text, [80, 30])

        for r in redBalls:
            if r == selectedBall:
                if r.vel.x > 1 or r.vel.x < -1 or r.vel.y > 1 or r.vel.y < -1:
                    canPlay = False
                elif (r.vel.x <= 1 or r.vel.x >= -1 or r.vel.y <= 1 or r.vel.y >= -1) and hasShot:
                    if switchPlayer:
                        changeTurn += 1
                        selectedBall = None
                    canPlay = True
                    switchPlayer = False
                    r.vel = Vec2(0, 0)

        for r in blueBalls:
            if r == selectedBall:
                if r.vel.x > 1 or r.vel.x < -1 or r.vel.y > 1 or r.vel.y < -1:
                    canPlay = False
                elif (r.vel.x <= 1 or r.vel.x >= -1 or r.vel.y <= 1 or r.vel.y >= -1) and hasShot:
                    if switchPlayer:
                        changeTurn += 1
                        selectedBall = None
                    canPlay = True
                    switchPlayer = False
                    r.vel = Vec2(0, 0)

        #print(redBalls)

        # Event Loop
        for e in pygame.event.get():
            # user clicks closed button
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and canPlay:  # left mouse button
                # Storing mouse x and y positions
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                if redTurn:
                    for r in redBalls:
                        print("red ", r)
                        sqx = (x - r.pos.x) ** 2
                        sqy = (y - r.pos.y) ** 2
                        if math.sqrt(sqx + sqy) < r.radius:
                            selectedBall = r
                            clickAndDrag = True
                    print("redBalls: ", redBalls)
                    print("redBallsCheck: ", redBallsCheck)
                    print("------------------")

                elif blueTurn:
                    for b in blueBalls:
                        print("blue ", blueBalls)
                        sqx = (x - b.pos.x) ** 2
                        sqy = (y - b.pos.y) ** 2
                        if math.sqrt(sqx + sqy) < b.radius:
                            selectedBall = b
                            clickAndDrag = True
                #print(selectedBall)

            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and canPlay:
                clickAndDrag = False
                # Add a velocity to the ball after release of mouse button
                if selectedBall is not None:
                    # Finding distance between two points, then to make ball follow line, gotta make it negative.
                    selectedBall.vel = (selectedBall.pos - Vec2(pygame.mouse.get_pos())) * 2
                    switchPlayer = True
                    hasShot = True
                    canPlay = False

        if clickAndDrag: #and selectedBall is not None:
            pygame.draw.line(screen, (0, 0, 0), selectedBall.pos, pygame.mouse.get_pos(), 2)

        # Shows changes to entire screen
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
