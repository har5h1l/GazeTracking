import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# question for asker
question = input('What do you want to ask?')
fontsize = 2 #later we will change this
answer = ''
selecting = 'Unselected'

# blink status
x = 0

# run application
while True:
    # open webcam
    _, frame = webcam.read()

    # check eyegaze position (refreshes every instance)
    gaze.refresh(frame)
    frame = gaze.annotated_frame()

    # add question
    cv2.putText(frame, question, (640, 360), cv2.FONT_HERSHEY_DUPLEX, fontsize, (255, 255, 255), 2)
    cv2.putText(frame, 'Left is No, Right is Yes', (640, 440), cv2.FONT_HERSHEY_DUPLEX, 1.4, (255, 255, 255), 2)
    cv2.putText(frame, 'Blink To Select', (640, 520), cv2.FONT_HERSHEY_DUPLEX, 1.4, (34, 139, 34), 2)

    # display answer
    if gaze.is_blinking(): 
        thickness = -1
        x += 1
        if x == 1: selecting = 'Selected'
    else:
        selecting = 'Unselected'
        thickness = 2
        x = 0
        if gaze.is_right(0.5): answer = 'Yes'
        elif gaze.is_left(0.5): answer = 'No'
    cv2.putText(frame, answer, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (255, 255, 255), 2)
    cv2.putText(frame, selecting, (90, 100), cv2.FONT_HERSHEY_DUPLEX, 1.6, (255, 255, 255), 2)

    # pupils
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, 'Left pupil:  ' + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 1)

    cv2.circle(frame, left_pupil, 30, (34, 139, 34), thickness)
    cv2.circle(frame, right_pupil, 30, (34, 149, 34), thickness)

    cv2.imshow('Demo', frame)

    if x == 15: 
        print(answer)
        break  

    if cv2.waitKey(1) == 27:
        break

webcam.release()
cv2.destroyAllWindows()
