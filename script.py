import cv2
import mediapipe as mp
import sys

# Initializing Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.6, min_tracking_confidence=0.9)

# Definition of the hand detection area (a little larger than the hand itself)
DETECTION_REGION = 70

# Definition of the maximum distance to consider a hand as a false detection
MAX_DISTANCE = DETECTION_REGION

# Add a variable to store currently detected hand positions
previous_hands = {}
previous_num_hands = 0

# Add a variable to store currently detected hand positions
current_hands = {}


# Function to detect hands in each frame
def detect_hands(frame):
    # Definition of variables for hand detection
    global previous_hands, previous_num_hands
    cx, cy = frame.shape[1] // 2, frame.shape[0] // 2

    # Set hand_landmarks to None
    hand_landmarks = None

    # Convert image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Hand detection with Mediapipe
    results = hands.process(image)

    # Checking if there is a detected hand
    if results.multi_hand_landmarks:
        # Loop on each detected hand
        for hand_landmarks in results.multi_hand_landmarks:
            # Recovery of the central position of the hand
            cx, cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1]), int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0])

            # Checking if this hand has already been detected
            is_new_hand = True
            for hand_id, hand_position in previous_hands.items():
                if hand_position is not None and abs(hand_position[0] - cx) < DETECTION_REGION and abs(hand_position[1] - cy) < DETECTION_REGION:
                    # The hand was previously detected, so we mark it as an existing hand and update its position
                    previous_hands[hand_id] = (cx, cy)
                    is_new_hand = False
                    break

            # If the hand is new, it is added to the dictionary of detected handss
            if is_new_hand:
                hand_id = max(previous_hands.keys(), default=-1) + 1
                previous_hands[hand_id] = (cx, cy)

            # Check if a hand has been removed and reappears nearby
            for hand_id, hand_position in previous_hands.items():
                if hand_position is not None and cx is None and cy is None:
                    # This is the first hand detected in this frame
                    cx, cy = hand_position
                    continue

                if hand_position is None:
                    # The hand is no longer detected
                    continue

                # Calculating the distance between the two hand positions
                distance = ((cx - hand_position[0]) ** 2 + (cy - hand_position[1]) ** 2) ** 0.5
                if distance < DETECTION_REGION:
                    # We conclude that it is the same hand
                    previous_hands[hand_id] = (cx, cy)
                    cx, cy = hand_position

    # Image Display with Detected Hands
    for hand_id, hand_position in previous_hands.items():
        if hand_position is not None:
            # Draw the skeleton of the hand
            if hand_landmarks is not None:
               for hand_id, hand_landmarks in zip(range(num_hands), results.multi_hand_landmarks):
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


    return frame, len([hand for hand in previous_hands.values() if hand is not None])

# Opening the video
cap = cv2.VideoCapture(sys.argv[1])

# Loop on each frame of the video
while cap.isOpened():
    # Frame recovery
    ret, frame = cap.read()

    # If the frame is successfully retrieved
    if ret:
        # In-frame hand detection
        frame, num_hands = detect_hands(frame)

        # Display of the number of hands detected in the frame
        cv2.putText(frame, f'Number of hands: {num_hands}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Frame display
        cv2.imshow('Video', frame)

        # If the 'q' key is pressed, the loop is exited
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Display of the total number of hands detected
            print(f"Total number of hands detected: {num_hands}")
            break
    else:
        # Display of the total number of hands detected
        print(f"Total number of hands detected: {num_hands}")
        break

# Close video and OpenCV windows
cap.release()
cv2.destroyAllWindows()
