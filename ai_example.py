import cv2
import os


class AI():
    def __init__(self, username):
        self.username = username
        self.folder = './dataset/{}'.format(self.username)
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        self.cam = cv2.VideoCapture(0)
        self.face_detector = cv2.CascadeClassifier(
            'haarcascade_frontalface_default.xml'
        )

    def configure(self):
        self.cam.set(3, 640)
        self.cam.set(4, 480)
        
    def run(self):
        img_counter = 0
        while img_counter <= 15:
            key = input("Press q to quit or ENTER to continue: ")
            if key == 'q':
                break
        
            ret, frame = self.cam.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, 1.3, 5)
        
            if(len(faces) == 0):
                print("No face detected, please try again")
                continue
        
            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
                img_name = "{}/{:04}.jpg".format(self.folder,img_counter)
                cv2.imwrite(img_name, frame[y:y+h,x:x+w])
                print("{} written!".format(img_name))
                img_counter += 1

    def __del__(self):
        self.cam.release()
        cv2.destroyAllWindows()