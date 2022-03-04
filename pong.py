import pygame
from paddle import Paddle
from ball import Ball
import time
import cv2
import mediapipe as mp
from pygame import display, movie

pygame.init()
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 700)
cap.set(4, 500)
mpHands = mp.solutions.hands
hands = mpHands.Hands()

# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("image")

paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = 20
paddleA.rect.y = 200

paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = 670
paddleB.rect.y = 200

ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

# This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Add the 2 paddles and the ball to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# Initialise player scores
scoreA = 0
scoreB = 0
valtozo = True
# camera
mpDraw = mp.solutions.drawing_utils
# cap = cv2.VideoCapture(0)
# mpHands = mp.solutions.hands
# hands = mpHands.Hands()

pTime = 0
cTime = 0
while carryOn:

    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                carryOn = False
    # ------------------------------------------------------------------------------------------
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if 300 < cx < 690:
                    paddleB.rect.y = cy
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for ko, fa in enumerate(handLms.landmark):
                z, s, n = img.shape
                nb, nj = int(fa.x * s), int(fa.y * z)
                if -50 < nb < 300:
                    paddleA.rect.y = nj
            # ------------------------------------------------------------------------------------------

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    all_sprites_list.update()

    # Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x >= 690:
        scoreA += 1
        ball.velocity[0] = -ball.velocity[0]
        ball.rect.x = 345
        ball.rect.y = 195
        paddleA.rect.x = 20
        paddleA.rect.y = 200
        paddleB.rect.x = 670
        paddleB.rect.y = 200
        valtozo = False
    if ball.rect.x <= 0:
        scoreB += 1
        ball.velocity[0] = -ball.velocity[0]
        ball.rect.x = 345
        ball.rect.y = 195
        paddleA.rect.x = 20
        paddleA.rect.y = 200
        paddleB.rect.x = 670
        paddleB.rect.y = 200
        valtozo = False
    if ball.rect.y > 490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 0:
        ball.velocity[1] = -ball.velocity[1]
    if scoreA == 10 or scoreB == 10:
        break
    # Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
        ball.bounce()

    # --- Drawing code should go here
    # First, clear the screen to black.

    screen.fill(BLACK)
    # Draw the net
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)

    # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen)

    # Display scores:
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (250, 10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (420, 10))

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3,(255,0,255),3)

    cv2.imshow("image", img)
    cv2.waitKey(1)
    #if valtozo == False:
        #time.sleep(2)
        #valtozo = True

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
