"""
facial_recognition.py

Modified by  Suwat Tangtragoonviwatt (s3710374)
            Laura Jonathan (s3696013)
            Warren Shipp (s3690682)
            Aidan Afonso (s3660805)


This script is intended to run facial recognition as an option for
users authentication

Acknowledgement
This code is adapted from:
https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826
"""
import os
import time
import pickle
import cv2
import imutils
from imutils import paths
from imutils.video import VideoStream
import face_recognition


class Capture():
    """
    Capture user image when for facial recognition login
    """
    def __init__(self, username):
        self.__username = username
        self.__folder = './dataset/{}'.format(self.__username)
        if not os.path.exists(self.__folder):
            os.makedirs(self.__folder)
        self.__cam = cv2.VideoCapture(0)
        self.__face_detector = cv2.CascadeClassifier(
            'haarcascade_frontalface_default.xml'
        )

    def configure(self):
        """
        Config camera
        """
        self.__cam.set(3, 640)
        self.__cam.set(4, 480)

    def run(self):
        """
        Run capture
        """
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
            ret, frame = self.__cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.__face_detector.detectMultiScale(gray, 1.3, 5)

            if not faces:
                print("No face detected, please try again")
                continue

            for (x_axis, y_axis, width, height) in faces:
                cv2.rectangle(
                    frame,
                    (x_axis, y_axis),
                    (x_axis + width, y_axis + height),
                    (255, 0, 0),
                    2
                )
                img_name = "{}/{:04}.jpg".format(self.__folder, img_counter)
                cv2.imwrite(
                    img_name,
                    frame[y_axis:y_axis+height, x_axis:x_axis+width]
                )
                print("{} written!".format(img_name))
                img_counter += 1
            time.sleep(0.5)

    def __del__(self):
        self.__cam.release()
        cv2.destroyAllWindows()


class Trainer():
    """
    Trainer Class to train the image captured by Capture Class
    Prepare for facial recognition login
    """
    def __init__(self):
        self.__folder = './dataset'
        self.__known_encodings = []
        self.__known_names = []

    def run(self):
        """
        Run the training
        """
        # grab the paths to the input images in our dataset
        print("[INFO] quantifying faces...")
        image_paths = list(paths.list_images(self.__folder))

        # loop over the image paths
        for (i, image_path) in enumerate(image_paths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(
                i + 1,
                len(image_paths)
            ))
            name = image_path.split(os.path.sep)[-2]

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(image_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(
                rgb,
                model="hog"
            )

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and
                # encodings
                self.__known_encodings.append(encoding)
                self.__known_names.append(name)

    def save(self):
        """
        dump the facial encodings + names to disk
        """
        print("[INFO] serializing encodings...")
        data = {
            "encodings": self.__known_encodings,
            "names": self.__known_names
        }
        file = open('encodings.pickle', "wb")
        file.write(pickle.dumps(data))
        file.close()


class Recogniser():
    """
    Recogniser class to detect if the face match the dataset
    """
    def __init__(self):
        self.__display = 1
        self.__user = ""
        self.__video_stream = VideoStream(src=0).start()
        self.__data = ""
        self.__writer = None
        self.__names = []

    def load(self):
        """
        Load trained data
        """
        # load the known faces and embeddings
        print("[INFO] loading encodings...")
        self.__data = pickle.loads(open('encodings.pickle', "rb").read())
        # initialize the video stream and pointer to output video file, then
        # allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        time.sleep(1.0)

    def encoding(self, rgb, boxes):
        """
        Encode data
        """
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(
                self.__data["encodings"],
                encoding
            )
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matched = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matched:
                    name = self.__data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

            # update the list of names
            self.__names.append(name)

    def run(self):
        """
        Run the recogniser
        """
        # loop over frames from the video file stream
        while True:
            # grab the frame from the threaded video stream
            frame = self.__video_stream.read()

            # convert the input frame from BGR to RGB then resize it to have
            # a width of 750px (to speedup processing)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(frame, width=240)
            rescale = frame.shape[1] / float(rgb.shape[1])

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input frame, then compute
            # the facial embeddings for each face
            boxes = face_recognition.face_locations(
                rgb,
                model="hog"
            )

            # run encoding
            self.encoding(rgb, boxes)

            # loop over the recognized faces
            for ((top, right, bottom, left), name) in zip(boxes, self.__names):
                # rescale the face coordinates
                top = int(top * rescale)
                right = int(right * rescale)
                bottom = int(bottom * rescale)
                left = int(left * rescale)

                # print to console, identified person
                if name:
                    self.__user = name
                    break
                # Set a flag to sleep the cam for fixed time
                time.sleep(1.0)

            # if the video writer is None *AND* we are supposed to write
            # the output video to disk initialize the writer
            if self.__writer is None and "output/capture.avi" is not None:
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                self.__writer = cv2.VideoWriter(
                    "output/capture.avi",
                    fourcc,
                    20,
                    (frame.shape[1], frame.shape[0]),
                    True
                )

            # if the writer is not None, write the frame with recognized
            # faces to disk
            if self.__writer is not None:
                self.__writer.write(frame)

            # check to see if we are supposed to display the output frame to
            # the screen
            if self.__display > 0:
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF

                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break
            if self.__writer is not None:
                self.__writer.release()
            if self.__user != "":
                return self.__user

    def __del__(self):
        # do a bit of cleanup
        cv2.destroyAllWindows()
        self.__video_stream.stop()
        # check to see if the video writer point needs to be released
