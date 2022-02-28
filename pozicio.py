import cv2
import mediapipe as mp
import time
from paddle import Paddle
class Pozi:
    def __init__(self, paddleA, paddleB):
        self.paddleA = paddleA
        self.paddleB = paddleB
        #--------------
        WHITE = (255,255,255)

        paddleA = Paddle(WHITE, 10, 100)
        paddleA.rect.x = 20
        paddleA.rect.y = 200
        
        paddleB = Paddle(WHITE, 10, 100)
        paddleB.rect.x = 670
        paddleB.rect.y = 200
        #------------------
        cap = cv2.VideoCapture(0)
        mpHands = mp.solutions.hands
        hands = mpHands.Hands()
        mpDraw = mp.solutions.drawing_utils
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
        def helyzet(self):    
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                        # print(id, lm)
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        #print(id, cx, cy)
                        if id == 8:
                            cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                        # Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B)
                        if 0 <= cx <= 300 and 0 <= cy <= 250:
                            return paddleA.moveUp(5)
                # bal felső sarok

                        if 0 <= cx <= 300 and 250 <= cy <= 500:
                            return paddleA.moveDown(5)
                # bal also sarok

                        if 300 <= cx <= 600 and 0 <= cy <= 250:
                            return paddleB.moveUp(5)
                # jobb felső

                        if 300 <= cx <= 600 and 250 <= cy <= 500:
                            return paddleB.moveDown(5)
                # jobb alsó
