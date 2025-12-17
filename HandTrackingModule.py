import cv2
import mediapipe as mp

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        """
        Initializes the MediaPipe Hands object.
        :param mode: False for video (faster), True for static images.
        :param maxHands: Maximum number of hands to detect.
        :param detectionCon: Minimum confidence value (0.0 to 1.0).
        :param trackCon: Minimum tracking confidence (0.0 to 1.0).
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        """
        Processes the image and detects hands.
        :param img: The image frame from the video.
        :param draw: Boolean, whether to draw the skeleton on the image.
        :return: The processed image with (or without) drawings.
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        """
        Extracts the coordinate list for a specific hand.
        :param img: The image frame.
        :param handNo: Index of the hand to track (0 is the first hand detected).
        :param draw: Boolean, whether to draw circles on the landmarks.
        :return: A list of [id, x, y] for all 21 points.
        """
        lmList = []
        if self.results.multi_hand_landmarks:
            # Pick the specific hand based on handNo
            if len(self.results.multi_hand_landmarks) > handNo:
                myHand = self.results.multi_hand_landmarks[handNo]
                
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    
                    # Append the ID and the Pixel Coordinates to our list
                    lmList.append([id, cx, cy])
                    
                    if draw:
                        # Draw a circle on every landmark
                        cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)

        return lmList


import math

def calculate_angle(p1, p2, p3):
    """
    Calculates the angle at p2 formed by p1-p2-p3
    Input: p1, p2, p3 are (x, y) tuples
    Output: Angle in degrees
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    # Calculate the angle
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                         math.atan2(y1 - y2, x1 - x2))
    
    # Handle negative angles to ensure we get a positive value
    if angle < 0:
        angle += 360
        
    # We generally want the acute angle (inside angle)
    if angle > 180:
        angle = 360 - angle
        
    return angle