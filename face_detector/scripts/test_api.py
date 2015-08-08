# import the necessary packages
import base64
import requests
import cv2

# define the URL to our face detection API
url = "http://localhost:8888/face_detection/detect/"

# use our face detection API to find faces in images via image URL
image = cv2.imread("DSCF4372.jpg")
payload = {"url": "http://www.pyimagesearch.com/wp-content/uploads/2015/05/obama.jpg"}
payload = {"url": "https://lh5.googleusercontent.com/-CkygPUVtHlg/VbFchipGzHI/AAAAAAAACoU/q6HAty1awSM/w825-h567-no/DSCF4372.jpg"}
payload = {"url": "https://lh3.googleusercontent.com/T_rSiNpp2clBIHHugHga9o981yeLRuLeRvBNzy0tjZs=w876-h657-no"}

payload = {"url": "https://lh4.googleusercontent.com/0VuTt-FTklUiQOaGN5cJrGXkP-5m1TIV1g0RxF6PiDU9rAGjrgdN0ZTTaoQTBEYNovUdHw=w1256-h537"}



r = requests.post(url, data=payload).json()
print "DSCF4372.jpg: {}".format(r)

# loop over the faces and draw them on the image
for (startX, startY, endX, endY) in r["faces"]:
	cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

# show the output image
#cv2.imshow("DSCF4372.jpg", image)
cv2.imwrite("DSCF4372_2.jpg", image)

#TODO: read the file convert to base64
r, buf = cv2.imencode(".jpg",image)
encoded_string = base64.b64encode(buf)

output = '<img src="data:image/jpeg;base64,%s"/>' % encoded_string

with open("output.html", "w") as text_file:
    text_file.write("<html><h1>hello</h1> <p>%s</p></html>" % output)

#print encoded_string
# with open("yourfile.ext", "rb") as image_file:
#     encoded_string = base64.b64encode(image.read())

#
# # load our image and now use the face detection API to find faces in
# # images by uploading an image directly
# image = cv2.imread("adrian.jpg")
# payload = {"image": open("adrian.jpg", "rb")}
# r = requests.post(url, files=payload).json()
# print "adrian.jpg: {}".format(r)
#
# # loop over the faces and draw them on the image
# for (startX, startY, endX, endY) in r["faces"]:
# 	cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
#
# # show the output image
# cv2.imshow("adrian.jpg", image)
# cv2.waitKey(0)