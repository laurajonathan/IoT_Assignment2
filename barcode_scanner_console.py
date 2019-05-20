# USAGE
# python3 barcode_scanner_console.py

## Acknowledgement
## This code is adapted from:
## https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
## pip3 install pyzbar

# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2

class QR_Scanner():
	def __init__(self):
		self.vs = VideoStream(src = 0).start()
		self.amount = ""
		self.isbn_list = ""

	def run(self):
		#ask the user how many books theyd like to return
		amount_string = input("How many books would you like to return?: ")
		while amount_string.isdigit() is not True:
			amount_string = input("Please enter a number or Enter to cancel: ")
			if amount_string.isdigit():
				self.amount = int(amount_string)
			if amount_string == "":
				return ""

		found = set()
		# count the number of books that have been scanned
		counter = 0
		# loop over the frames from the video stream
		while counter < self.amount:
			# grab the frame from the threaded video stream and resize it to
			# have a maximum width of 400 pixels
			frame = self.vs.read()
			frame = imutils.resize(frame, width = 400)

			# find the barcodes in the frame and decode each of the barcodes
			barcodes = pyzbar.decode(frame)

			# loop over the detected barcodes
			for barcode in barcodes:
				# the barcode data is a bytes object so we convert it to a string
				barcodeData = barcode.data.decode("utf-8")
				barcodeType = barcode.type

				# if the barcode text has not been seen before print it and update the set
				#if barcodeData.rstrip() not in found:
				print("[FOUND] Type: {}, Data: {}".format(barcodeType, barcodeData))
				found.add(barcodeData.rstrip())
				counter += 1
		
			# wait a little before scanning again
			time.sleep(2)

		# iterate through the set and combine all isbn numbers into a string seperated by |
		new_count = 0
		for item in found:
			if new_count+1 < self.amount:
				item += "|"
				isbn_list += item
			else:
				isbn_list += item
			new_count += 1
		# close the output CSV file do a bit of cleanup
		print("[INFO] cleaning up...")
		self.vs.stop()
		return isbn_list