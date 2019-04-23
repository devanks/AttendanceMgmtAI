from django.shortcuts import render
# import the necessary packages
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.http import JsonResponse
import numpy as np
import urllib
import json
import cv2
import face_recognition
import pickle

from django.urls import reverse_lazy

from .forms import CustomUserCreationForm

from django.contrib.auth.decorators import user_passes_test

def check_if_teacher(user):
    return user.is_staff
# def email_check(user):
    # return user.email.endswith('@nitc.ac.in')

# @user_passes_test(email_check)
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('account_login')
    template_name = 'signup.html'


class HomePageView(generic.TemplateView):
    template_name = 'home.html'

@user_passes_test(check_if_teacher, login_url='/accounts/login/?=access-denied-for-students/', redirect_field_name=None)
class UploadTestView(generic.TemplateView):
    template_name = 'simple_upload.html'

class StudentHomePageView(generic.TemplateView):
    template_name = 'test.html'

@user_passes_test(check_if_teacher, login_url='/accounts/login/?=access-denied-for-students/', redirect_field_name=None)
class TeacherHomePageView(generic.TemplateView):
    template_name = 'test.html'

@user_passes_test(check_if_teacher, login_url='/accounts/login/?=access-denied-for-students/', redirect_field_name=None)
@csrf_exempt
def detect(request):
    # initialize the data dictionary to be returned by the request
    data = {"success": False}
    template = "simple_upload.html"
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
            image = _grab_image(url=url)

        ### START WRAPPING OF COMPUTER VISION APP
        # Insert code here to process the image and update
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        faceSET = pickle.loads(open("test5.pickle","rb").read())
        boxes = face_recognition.face_locations(rgb,model="hog") # REMEMBER TO CHANGE TO CNN
        encodings = face_recognition.face_encodings(rgb, boxes)
        
        names = []

        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(faceSET["encodings"],
                encoding,0.47)
                # encoding,0.5)
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
                    name = faceSET["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number of
                # votes (note: in the event of an unlikely tie Python will
                # select first entry in the dictionary)
                name = max(counts, key=counts.get)
            
            # update the list of names
            names.append(name)
        # the `data` dictionary with your results
        ### END WRAPPING OF COMPUTER VISION APP

        # update the data dictionary
        data["success"] = True
        data["names"] = names
    # return a JSON response
    return JsonResponse(data)


# NEED NOT BE CHANGED
def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    if path is not None:
        image = cv2.imread(path)

    # otherwise, the image does not reside on disk
    else:    
        # if the URL is not None, then download the image
        if url is not None:
            resp = urllib.request.urlopen(url)
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