# Import the pygame library and initialise the game engine
from pozicio import Pozi
import pygame
from paddle import Paddle
from ball import Ball
import time
import cv2
import mediapipe as mp
pygame.init()
 
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
 
# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
 
paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = 20
paddleA.rect.y = 200
 
paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = 670
paddleB.rect.y = 200
 
ball = Ball(WHITE,10,10)
ball.rect.x = 345
ball.rect.y = 195
 
#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
 
# Add the 2 paddles and the ball to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)
 
# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
 
#Initialise player scores
scoreA = 0
scoreB = 0
valtozo = True
#camera
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
# -------- Main Program Loop -----------
while carryOn:

    
    if valtozo == False:
        time.sleep(2)
        valtozo = True
    
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     carryOn=False
    
    
    
    #mpDraw = mp.solutions.drawing_utils
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                #if id == 8:
                    #cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
        # Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B)
                if 0 <= cx <= 300 and 0 <= cy <= 250:
                    paddleA.moveUp(1)
        # bal felső sarok

                if 0 <= cx <= 300 and 250 <= cy <= 500:
                    paddleA.moveDown(1)
        # bal also sarok

                if 300 <= cx <= 600 and 0 <= cy <= 250:
                    paddleB.moveUp(1)
        # jobb felső

                if 300 <= cx <= 600 and 250 <= cy <= 500:
                    paddleB.moveDown(1)
        # jobb alsó
    """
    #Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B) 
    

    keys = pygame.key.get_pressed()
    #playerA
    if keys[pygame.K_w]:
        paddleA.moveUp(5)
    if keys[pygame.K_s]:
        paddleA.moveDown(5)
    #playerB
    if keys[pygame.K_UP]:
        paddleB.moveUp(5)
    if keys[pygame.K_DOWN]:
        paddleB.moveDown(5)    
    """
    # --- Game logic should go here
    all_sprites_list.update()
    
    #Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x>=690:
        scoreA+=1
        ball.velocity[0] = -ball.velocity[0]
        ball.rect.x = 345
        ball.rect.y = 195
        paddleA.rect.x = 20
        paddleA.rect.y = 200
        paddleB.rect.x = 670
        paddleB.rect.y = 200
        valtozo = False
    if ball.rect.x<=0:
        scoreB+=1
        ball.velocity[0] = -ball.velocity[0]
        ball.rect.x = 345
        ball.rect.y = 195
        paddleA.rect.x = 20
        paddleA.rect.y = 200
        paddleB.rect.x = 670
        paddleB.rect.y = 200
        valtozo = False
    if ball.rect.y>490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1]     
    if scoreA == 10 or scoreB == 10:
            break
    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
      ball.bounce()
    
    # --- Drawing code should go here
    # First, clear the screen to black. 
    screen.fill(BLACK)
    #Draw the net
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
    
    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen) 
 
    #Display scores:
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (250,10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (420,10))
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(60)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()