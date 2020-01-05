import pygame
from Forces import Gravitation
from Vec2 import Vec2
from circle import Circle
from Polygon import UniformPolygon
import random
from Wall import Wall
from timeit import default_timer as timer
from Contact2 import contact2
from math import *
import itertools
from Contact import contact

objects = []
asteroidOffsets = []
ringOffsets = []
forces = []
obstacles = []
checkpoints = []
randomLoc = []
G = 6.7 * 10**-5
rocketMass = 1
ring = []

GREEN = [0, 255, 0]
BLACK = [0, 0, 0]
GREY = [100, 100, 100]
WHITE = (255, 255, 255)
PURPLE = [30, 0, 30]

earth_radius = 63.7

screen = pygame.display.set_mode(size=[1500, 800])

earthMass = 5.972 * 10 ** 24


def createAsteroid(playerPos):
    asteroidOffsets.clear()  # clearing the offsets list

    # Creating the asteroid offsets
    for i in range(12):
        x = 6 * cos(i * pi / 6)
        y = 6 * sin(i * pi / 6)
        asteroidOffsets.append(Vec2(x, y))
    asteroidOffsets.reverse()

    # Random ranges to spawn asteroids
    random1 = random.randint(-300, -100)
    random2 = random.randint(900, 1100)
    for i in range(4):
        randomLoc.append(random1)
        randomLoc.append(random2)
    randomX = random.choice(randomLoc)
    randomY = random.choice(randomLoc)
    randomRadius = random.randint(3, 15)
    randomPosition = Vec2(randomX, randomY)
    towardsPlayer = playerPos - randomPosition
    if towardsPlayer.x > 30 or towardsPlayer.y > 30 or towardsPlayer.x < -30 or towardsPlayer.y < -30:
        towardsPlayer *= Vec2(0.5, 0.5)
    asteroid = UniformPolygon(color=(200, 200, 200), pos=randomPosition, vel=towardsPlayer, mass=randomRadius * 3, offsets=asteroidOffsets)
    obstacles.append(asteroid)
    objects.append(asteroid)


def main():
    # Set up pygame and window
    pygame.init()
    forces = []
    walls = []
    # Set background color
    bg_color = PURPLE
    # Set the screen size
    screen.fill(bg_color)

    winCondition = False
    lossCondition = False

    timeLimit = 60
    startTimer = pygame.time.get_ticks()

    # Walls
    walls.append(Wall(pos=Vec2(0, 400), normal=Vec2(1, 0), length=400))
    walls.append(Wall(pos=Vec2(1500, 400), normal=Vec2(-1, 0), length=400))
    walls.append(Wall(pos=Vec2(400, 0), normal=Vec2(0, 1), length=400))
    walls.append(Wall(pos=Vec2(400, 800), normal=Vec2(0, -1), length=400))

    up = False
    down = False
    left = False
    right = False
    spacebar = False
    spacePressed = False

    # Game Loops
    running = True
    # clock within pygame
    clock = pygame.time.Clock()
    # Set the fps of the game to 60
    fps = 60
    dt = 1 / fps

    black_hole = Circle(radius=100, color=BLACK, pos=Vec2(750, 400), mass=100000000000)
    objects.append(black_hole)

    ringOffsets.clear()

    for i in range(12):
        x = 70 * cos(i * pi / 6)
        y = 70 * sin(i * pi / 6)
        ringOffsets.append(Vec2(x, y))
    ringOffsets.reverse()

    for i in range(2):
        x = 200
        if i is 0:
            ring.append(UniformPolygon(color=GREY, pos=Vec2(x, 400), mass=100000000000, vel=Vec2(0, -110), offsets=ringOffsets))
        if i is 1:
            ring.append(UniformPolygon(color=GREY, pos=Vec2(1500 - x, 400), mass=100000000000, vel=Vec2(0, 110), offsets=ringOffsets))

    for r in ring:
        objects.append(r)




    rocketOffsets = [Vec2(-10, 0), Vec2(0, -20), Vec2(10, 0)]
    rocketCircle = Circle(10, WHITE, pos=Vec2(500, 160), mass=10)

    rocket = UniformPolygon(pos=Vec2(400, (600-63.7)), vel=Vec2(0, 0), offsets=rocketOffsets, color=WHITE, mass=rocketMass, width=0)
    objects.append(rocket)

    grav = Gravitation(objects, G)
    forces.append(grav)

    counter = 0

    font = pygame.font.SysFont('Calibri', 20, True, False)

    health = 500

    playerLose = False

    while running:
        for o in objects:
            o.clear_force()

        for f in forces:
            f.apply()

        for o in objects:
            o.update(dt)

        timerCount = timeLimit - ((pygame.time.get_ticks() - startTimer) / 1000)
        timerCount = round(timerCount, 1)

        currentTime = int(timer())
        if currentTime % 2 == 0:
            if counter <= 2:
                createAsteroid(rocket.pos)
                currentTime += 1
                counter += 1
        elif currentTime % 2 == 1:
            counter = 0

        screen.fill(bg_color)

        for o in objects:
            o.draw(screen)

        for o in obstacles:
            o.update(dt)
            o.draw(screen)

        for r in ring:
            r.update(dt)
            r.draw(screen)

        if not spacePressed:
            pygame.draw.rect(screen, (255, 255, 255), (500, 730, 503, 20), 1)
            pygame.draw.rect(screen, (255, 0, 0), (501, 731, health, 17), 0)

        for a, b in itertools.combinations(objects, 2):
            contact(a, b, restitution=0.2)

        for o in objects:
            distanceFromPlayer = o.pos - rocket.pos
            if distanceFromPlayer.mag() > 2000:
                objects.remove(o)

        for o in obstacles:
            distanceFromBlackHole = o.pos - black_hole.pos
            if distanceFromBlackHole.mag() < 70:
                obstacles.remove(o)
                objects.remove(o)

        shipFromBlackHole = rocket.pos - black_hole.pos
        if shipFromBlackHole.mag() < 70 and playerLose == False:
            objects.remove(rocket)
            playerLose = True
            health = 0

        for o in obstacles:
            asteroidDistanceFromRocket = o.pos - rocket.pos
            if asteroidDistanceFromRocket.mag() < 20 and health > 0:
                health -= 50

        rocketCircle.pos = rocket.pos

        for w in walls:
            contact2(rocketCircle, w)
            if rocket.pos.x > 1500:
                rocket.vel = Vec2(0, 0)
            if rocket.pos.x < 0:
                rocket.vel = Vec2(0, 0)
            if rocket.pos.y > 800:
                rocket.vel = Vec2(0, 0)
            if rocket.pos.y < 0:
                rocket.vel = Vec2(0, 0)

        if spacebar:
            objects.remove(rocket)
            spacePressed = True
            spacebar = False

        if health == 0:
            rocketVelocityText = font.render("You Lose", True, (255, 255, 255))
            screen.blit(rocketVelocityText, [700, 200])
            if not lossCondition and playerLose == False:
                objects.remove(rocket)
            lossCondition = True


        if right:
            rocket.vel.x += 5
        if left:
            rocket.vel.x -= 5
        if up:
            rocket.vel.y -= 5
        if down:
            rocket.vel.y += 5

        for e in pygame.event.get():
            # user clicks closed button
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    right = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    left = True
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    right = False
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    left = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if winCondition and not lossCondition:
                        rocket.vel = Vec2(0, -10000)
                        spacebar = True

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    up = True
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_UP:
                    up = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    down = True
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_DOWN:
                    down = False

        timerText = font.render("TIME UNTIL ESCAPE: " + str(timerCount), True, WHITE)
        objectiveText = font.render("While studying a black hole, a sudden asteroid shower has appeared! Survive for 60 seconds while your lightspeed engine powers up to escape!", True, WHITE)
        if timerCount > 55:
            screen.blit(objectiveText, [200, 150])
        if timerCount <= 0 and not lossCondition:
            if not spacePressed:
                objectiveText = font.render("Quick! Press Spacebar to jump to lightspeed!", True, WHITE)
                screen.blit(objectiveText, [500, 150])
            winCondition = True
            timerText = font.render("0", True, WHITE)
        if spacePressed:
            objectiveText = font.render(" ", True, WHITE)
            screen.blit(objectiveText, [200, 100])
            winText = font.render("Congratulations! You escaped!", True, WHITE)
            screen.blit(winText, [650, 200])
            health = 500

        screen.blit(timerText, [20, 20])


        pygame.display.flip()
        clock.tick(fps) / 1000
    pygame.quit()

# Safe start
if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise
