"""
qr_code_scanner.py

Modified by  Suwat Tangtragoonviwatt (s3710374)
            Laura Jonathan (s3696013)
            Warren Shipp (s3690682)
            Aidan Afonso (s3660805)


This script is intended to run object recognition as an option for
qr code scanning rather than manual input

Acknowledgement
This code is adapted from:
https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
"""

import time
import imutils
from imutils.video import VideoStream
from pyzbar import pyzbar


class QRCodeScanner():
    """
    QR Code Scanner class
    Detect QR Code Object then extract the message inside
    """
    def __init__(self):
        self.__video_stream = VideoStream(src=0).start()
        self.amount = 0

    def setup(self):
        """
        Setup the config
        """
        # ask the user how many books theyd like to return
        amount_string = input("How many books would you like to return?: ")
        if amount_string.isdigit() is True:
            self.amount = int(amount_string)
        while amount_string.isdigit() is not True:
            amount_string = input("Please enter a number or Enter to cancel: ")
            if amount_string.isdigit():
                self.amount = int(amount_string)
            if amount_string == "":
                return ""

    def run(self):
        """
        Run QR Code Scanner
        """

        found = list()
        # count the number of books that have been scanned
        counter = 0
        # loop over the frames from the video stream
        print("Please scan your first book....")
        while counter < self.amount:
            # grab the frame from the threaded video stream and resize it to
            # have a maximum width of 400 pixels
            frame = self.__video_stream.read()
            frame = imutils.resize(frame, width=400)

            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)

            # loop over the detected barcodes
            for barcode in barcodes:
                # the barcode data is a bytes object
                # so we convert it to a string
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type

                # if the barcode text has not been seen before
                # print it and update the set
                # if barcodeData.rstrip() not in found:
                print("[FOUND] Type: {}, Data: {}".format(
                    barcode_type,
                    barcode_data
                ))
                found.append(barcode_data.rstrip())
                counter += 1

            # wait a little before scanning again
            time.sleep(2)

        # iterate through the set and
        # combine all isbn numbers into a string seperated by |
        return "|".join(found)

    def __del__(self):
        # close the output CSV file do a bit of cleanup
        self.__video_stream.stop()
