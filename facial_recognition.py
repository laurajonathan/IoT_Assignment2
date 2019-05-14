# USAGE
# With default parameter of user/id
#       python3 01_capture.py -n default_user
# OR specifying the dataset and user/id
#       python3 02_capture.py -i dataset -n default_user

## Acknowledgement
## This code is adapted from:
## https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826

# import the necessary packages
# import the necessary packages
import cv2
import os
from imutils import paths
import face_recognition
import pickle
from imutils.video import VideoStream
import imutils
import time

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
        count = 1
        key = input("Press q to quit or ENTER to continue: ")
        if key == 'q':
            return
        print("Look at the camera! :)")
        while count < 4:
            print(str(count)+"...")
            count += 1
            time.sleep(1.0)
            if count == 3:
                print("Smile!")

        while img_counter <= 15:
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
            time.sleep(0.5)

    def __del__(self):
        self.cam.release()
        cv2.destroyAllWindows()

class Trainer():
    def __init__(self):
        self.folder = './dataset'
    
    def run(self):
        # grab the paths to the input images in our dataset
        print("[INFO] quantifying faces...")
        imagePaths = list(paths.list_images(self.folder))

        # initialize the list of known encodings and known names
        knownEncodings = []
        knownNames = []

        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1,
                len(imagePaths)))
            name = imagePath.split(os.path.sep)[-2]

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb,
                model="hog")

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and
                # encodings
                knownEncodings.append(encoding)
                knownNames.append(name)

        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open('encodings.pickle', "wb")
        f.write(pickle.dumps(data))
        f.close()

class Recogniser():
    def __init__(self):
        self.display = 1
        self.user = ""
        self.vs = VideoStream(src=0).start()

    def run(self):
        # load the known faces and embeddings
        print("[INFO] loading encodings...")
        data = pickle.loads(open('encodings.pickle', "rb").read())

        # initialize the video stream and pointer to output video file, then
        # allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        writer = None
        time.sleep(1.0)

        # loop over frames from the video file stream
        while True:
            # grab the frame from the threaded video stream
            frame = self.vs.read()

            # convert the input frame from BGR to RGB then resize it to have
            # a width of 750px (to speedup processing)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(frame, width=240)
            r = frame.shape[1] / float(rgb.shape[1])

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input frame, then compute
            # the facial embeddings for each face
            boxes = face_recognition.face_locations(rgb,
                    model="hog")
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"],
                        encoding)
                name = "Unknown"

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key=counts.get)

                # update the list of names
                names.append(name)

            # loop over the recognized faces
            for ((top, right, bottom, left), name) in zip(boxes, names):
                # rescale the face coordinates
                top = int(top * r)
                right = int(right * r)
                bottom = int(bottom * r)
                left = int(left * r)

                # draw the predicted face name on the image
                #cv2.rectangle(frame, (left, top), (right, bottom),
                    #(0, 255, 0), 2)
                #y = top - 15 if top - 15 > 15 else top + 15
                #cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                #	0.75, (0, 255, 0), 2)
                
                # print to console, identified person
                if name:
                    self.user = name
                
                break
                # Set a flag to sleep the cam for fixed time
                time.sleep(1.0)


            # if the video writer is None *AND* we are supposed to write
            # the output video to disk initialize the writer
            if writer is None and "output/capture.avi" is not None:
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter("output/capture.avi", fourcc, 20, (frame.shape[1], frame.shape[0]), True)

            # if the writer is not None, write the frame with recognized
            # faces to disk
            if writer is not None:
                writer.write(frame)

            # check to see if we are supposed to display the output frame to
            # the screen
            if self.display > 0:
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF

                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break
            if writer is not None:
                writer.release()
            if self.user != "":
                return self.user

    def __del__(self):
        # do a bit of cleanup
        cv2.destroyAllWindows()
        self.vs.stop()
        # check to see if the video writer point needs to be released
        
