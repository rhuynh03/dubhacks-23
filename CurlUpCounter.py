import cv2
import mediapipe as mp
import numpy as np
import BasicPoseModule as pm


class CurlUpCounter(object):

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        detector = pm.poseDetector()
        count = 0
        direction = 0
        form = 0
        feedback = "Fix Form"


        while self.cap.isOpened():
            ret, img = self.cap.read() #640 x 480
            img =cv2.flip(img, 1)
            #Determine dimensions of video - Help with creation of box in Line 43
            width  = self.cap.get(3)  # float `width`
            height = self.cap.get(4)  # float `height`
            # print(width, height)

            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            # print(lmList)
            if len(lmList) != 0:
                hip = detector.findAngle(img, 11, 23, 25)
                knee = detector.findAngle(img, 23, 25, 27)

                #Percentage of success of curl up
                per = np.interp(hip, (70, 100), (0, 100))

                #Bar to show curl up progress
                bar = np.interp(hip, (70, 100), (380, 50))

                #Check to ensure right form before starting the program
                if hip > 105 and knee < 105:
                    form = 1

                #Check for full range of motion for the curlup
                if form == 1:
                    if per == 0:
                        if hip <= 65 and knee < 105:
                            feedback = "Down"
                            if direction == 0:
                                count += 0.5
                                direction = 1
                        else:
                            feedback = "Fix Form"

                    if per == 100:
                        if hip > 105 and knee < 105:
                            feedback = "Up"
                            if direction == 1:
                                count += 0.5
                                direction = 0
                        else:
                            feedback = "Fix Form"
                                # form = 0



                print(count)

                #Draw Bar
                if form == 1:
                    cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                    cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 0, 0), 2)


                #Curlup counter
                cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                            (255, 0, 0), 5)

                #Feedback
                cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
                cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                            (0, 255, 0), 2)


            cv2.imshow('Curlup counter', img)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
