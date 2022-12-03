import pygame
import random
from pygame import mixer  # for music

pygame.init()

screen = pygame.display.set_mode((561, 690))  # (width, height)

mixer.music.load("backgroundMusic.mp3")
mixer.music.play(-1)

run = True
scoreValue = 0
speed = 0.2  # change the starting speed as per your need
vehiclesOnScreen = 2

background = pygame.image.load('background.png')

pygame.display.set_caption("Race Car")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

scoreFont = pygame.font.Font('freesansbold.ttf', 32)

player = pygame.image.load('player.png')
playerX = 20
playerY = 450  # fixed

car = []
carX = [205, 405, 0, 0, 0]
carY = [200, 450, 0, 0, 0]
array = []  # contains index of cars that are currently running on screen
negArray = []  # contains index of cars that are currently not running on screen


car.append(pygame.image.load('blueCar.jpg'))

car.append(pygame.image.load('blackCar.jpg'))

car.append(pygame.image.load('greenCar.jpg'))

car.append(pygame.image.load('plane.jpg'))

car.append(pygame.image.load('booster.png'))


def playerPosition(x, y):
    screen.blit(player, (x, y))


def carPosition(x, y, i):
    screen.blit(car[i], (x, y))


def checkOverwrite():  # to check if a car is overwriting on other car
    for f in array:
        if (carY[f] > 0) and (carY[f] < 150):
            return True
    return False


def addVehicle():  # adds vehicle to the screen randomly
    choice = random.choice(negArray)
    array.append(choice)
    negArray.remove(choice)
    carY[choice] = 1
    if choice != 4:
        carX[choice] = random.choice([20, 205, 405])
    else:
        carX[choice] = random.choice([50, 235, 435])


def progress():  # increasing difficulty as the game progresses
    global speed, vehiclesOnScreen

    if scoreValue <= 20:
        speed = speed
    elif scoreValue <= 60:
        vehiclesOnScreen = 3
    elif scoreValue <= 100:
        speed = 1.5 * speed
    elif scoreValue <= 150:
        speed = (speed / 1.5) * 2
    elif scoreValue <= 250:
        vehiclesOnScreen = 4
    else:
        speed = (speed / 2) * 2.5


def crash():  # to be called once a car crashes with another car
    gameOverScreen = pygame.display.set_mode(
        (600, 600))  # initialising a new screen

    totalScoreFont = pygame.font.Font('freesansbold.ttf', 64)
    totalScore = totalScoreFont.render(
        "Score : " + str(scoreValue), True, (255, 255, 255))
    gameOverFont = pygame.font.Font('freesansbold.ttf', 64)
    gameOver = gameOverFont.render("GAME OVER", True, (255, 255, 255))
    mixer.music.load("gameOverSound.mp3")
    mixer.music.play(-1)

    running = True

    while running:
        gameOverScreen.fill((0, 0, 0))
        gameOverScreen.blit(gameOver, (100, 200))
        gameOverScreen.blit(totalScore, (100, 300))

        for crashEvent in pygame.event.get():

            if crashEvent.type == pygame.QUIT:
                running = False

        pygame.display.update()


while run:

    screen.blit(background, (0, 0))

    score = scoreFont.render(
        "Score : " + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # quit option
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if playerX == 205:
                    playerX = 20
                elif playerX == 405:
                    playerX = 205
            if event.key == pygame.K_RIGHT:
                if playerX == 20:
                    playerX = 205
                elif playerX == 205:
                    playerX = 405

    playerPosition(playerX, playerY)

    # code from line 141 to line 161 filter out the cars that are currently running on the screen from those that aren't

    k = 0
    p = 0

    for j in range(5):
        if carY[j] > 0:
            if k < len(array):
                array[k] = j
            else:
                array.append(j)
            k += 1
        else:
            if p < len(negArray):
                negArray[p] = j
            else:
                negArray.append(j)
            p += 1

    if k < len(array):
        del array[k:len(array)]
    if p < len(negArray):
        del negArray[p:len(negArray)]

    if len(array) < vehiclesOnScreen:
        if len(array) == 0:
            addVehicle()
        elif checkOverwrite() is False:
            addVehicle()

    for i in array:  # looping through 'array' list

        carY[i] += speed  # managing speed by increasing Y coordinate

        carPosition(carX[i], carY[i], i)

        if i != 4:
            # resizing required
            if (playerX == carX[i]) and ((playerY < (carY[i] + 115)) and (playerY > (carY[i] - 115))):
                crash()
                run = False
                break
        # resizing required
        elif ((playerX + 30) == carX[i]) and ((playerY < (carY[i] + 60)) and (playerY > (carY[i] - 60))):
            scoreValue += 10
            progress()
            carY[i] = 0
            break

        if carY[i] >= 690:  # if car runs out of screen
            carY[i] = 0

    pygame.display.update()  # updating screen throughout while loop
