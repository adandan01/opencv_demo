# import the necessary packages
import base64
import urllib
import os
from cv2.cv import Scalar

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
import cv2



# define the path to the face detector
FACE_DETECTOR_PATH = "{base_path}/cascades/haarcascade_frontalface_default.xml".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))


@csrf_exempt
def detect(request):
    # initialize the data dictionary to be returned by the request
    data = {"success": False}

    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        if request.FILES.get("image", None) is not None:
            # grab the uploaded image
            image = _grab_image(stream=request.FILES["image"])

        # otherwise, assume that a URL was passed in
        else:
            # grab the URL from the request
            url = request.POST.get("url", None)

            # if the URL is None, then return an error
            if url is None:
                data["error"] = "No URL provided."
                return JsonResponse(data)

            # load the image and convert
            if not url.startswith('http'):
                url ='http://localhost:9000' + url
            image = _grab_image(url=url)

        # convert the image to grayscale, load the face cascade detector,
        # and detect faces in the image
        new_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
        rects = detector.detectMultiScale(new_image, scaleFactor=1.1, minNeighbors=5,
                                          minSize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

        # construct a list of bounding boxes from the detection
        rects = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in rects]

        for (startX, startY, endX, endY) in rects:
            cv2.rectangle(image, (startX, startY), (endX, endY), Scalar(0, 255, 0), 2)


            # TODO: read the file convert to base64
        r, buf = cv2.imencode(".jpg", image)
        encoded_string = base64.b64encode(buf)

        output = 'data:image/jpeg;base64,%s' % encoded_string
        data.update({"num_faces": len(rects), "faces": rects, "success": True, 'image_data': output})

    # return a JSON response
    return JsonResponse(data)


def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    if path is not None:
        image = cv2.imread(path)

    # otherwise, the image does not reside on disk
    else:
        # if the URL is not None, then download the image
        if url is not None:
            resp = urllib.urlopen(url)
            data = resp.read()

        # if the stream is not None, then the image has been uploaded
        elif stream is not None:
            data = stream.read()

        # convert the image to a NumPy array and then read it into
        # OpenCV format
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image
