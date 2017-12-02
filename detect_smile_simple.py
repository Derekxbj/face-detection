# python detect_smile.py --cascade haarcascade_frontalface_default.xml \
# 	--model output/lenet.hdf5 

# import the packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2
from datetime import datetime

def detect_smile():
	# the arguments we need 
	# ap = argparse.ArgumentParser()
	# ap.add_argument("-c", "--cascade", required=True,
	# 	help="path to where the face cascade resides")
	# ap.add_argument("-m", "--model", required=True,
	# 	help="path to pre-trained smile detector CNN")
	# ap.add_argument("-v", "--video",
	# 	help="path to the (optional) video file")
	# args = vars(ap.parse_args())

	# load the face detector cascade and smile detector model
	# the smile detector has been pre-trained
	detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	model = load_model("output/lenet.hdf5")

	# # if a video path is not supplied, refer to the webcam
	# if not args.get("video", False):
	# 	camera = cv2.VideoCapture(0)

	# # else, load the video
	# else:
	# 	camera = cv2.VideoCapture(args["video"])

	camera = cv2.VideoCapture(0)
	tic = datetime.now()
	count = 0

	# loop it and get continous output
	while True:

		# grap the current frame
		(grabbed, frame) = camera.read()

		# I use it to test with video, not useful for webcam
		# if args.get("video") and not grabbed:
		# 	break

		# resize the frame to we want, and convert it to grayscale
		frame = imutils.resize(frame, width=350)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# clone the current frame
		frameClone = frame.copy()

		# apply face detector in the current frame,
		rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
			minNeighbors=5, minSize=(30, 30),
			flags=cv2.CASCADE_SCALE_IMAGE)

		# loop the face in the bounding boxes
		# the fX, fY, fW, fH is returned by the detectMultiScale method
		for (fX, fY, fW, fH) in rects:
			# extract the ROI of the face from the grayscale image
			roi = gray[fY:fY + fH, fX:fX + fW]
			# resize it to (28, 28)
			roi = cv2.resize(roi, (28, 28))
			roi = roi.astype("float") / 255.0
			roi = img_to_array(roi)
			roi = np.expand_dims(roi, axis=0)
			# prepare the ROI for classification via CNN

			# determine the probabilities of both "smiling" and "not smiling"
			(notSmiling, smiling) = model.predict(roi)[0]
	 		# Set the label
			label = "Smiling" if smiling > notSmiling else "Not Smiling"
			if label == "Smiling":
				count += 1


			# display the label and use the bounding box on the output frame
			cv2.putText(frameClone, label, (fX, fY - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
			cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH),
				(0, 0, 255), 2)

		# display the detected faces along with the labels
		cv2.imshow("Face", frameClone)

		# press q to quit the loop
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break

		# we make the scenerio to run the CNN for a period of time
		toc = datetime.now()
		if (toc-tic).total_seconds() > 7:
			break
		# print('Elapsed time: %f seconds' % (toc-tic).total_seconds())
		# print(count)

	camera.release()
	cv2.destroyAllWindows()

	return count

# count = detect_smile() 
# print(count)