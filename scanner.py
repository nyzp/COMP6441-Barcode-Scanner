from pyzbar import pyzbar
import numpy as np
import pytesseract
from PIL import Image
import face_recognition
from termcolor import colored
import cv2

database = {
    "X1537844312103": {
    "name": "Magan Leong",
    "age": "23",
    "zid": "5378443",
    "photo": "photos/magan.jpg"
    },

    "X1536427712109": {
    "name": "Bryan Huang",
    "age": "22",
    "zid": "5364277",
    "photo": "photos/bryan.jpg"
    }
}

# Functions
def decode(image):
    barcodeImg = imageProcessing(image)
    decodedObjects = pyzbar.decode(barcodeImg)
    flag = False
    check = False
    for obj in decodedObjects:

        # Print info about barcode (Diagnostic)
        #print("Scanned Barcode: ", obj)
        #print("Data: ", obj.data)

        # Check Barcode Type
        print("----------------------------------------------------------")
        print("Barcode Type:", obj.type)
        if obj.type != 'CODE39':
            print("Wrong ID Type!\n")
        else:
            # Aunthenticate ID
            check = authenticate(obj, image)

        if check is False:
            print(colored("Fake ID detected!\n", 'red'))
        else:
            print(colored("Legitimate ID!\n", 'green'))

        # Check for presence of Barcode
        if obj is not None:
            flag = True

    return image, flag

def imageProcessing(img):
    # Increase Brightness
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    value = 40
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    # Increase Contrast
    clip_limit = 2.0
    tile_grid_size = (8,8)
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid_size))
    cl = clahe.apply(l_channel)
    limg = cv2.merge((cl,a,b))

    image = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    return image

def faceDetection(image, photo):

     # Grab Photo from ID
    faceScan = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = faceScan.detectMultiScale(image, 1.3, 5)
    for (x,y,w,h) in faces:

        # Slice the face from the image
        face = image[y:y+h, x:x+w]
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        image = cv2.filter2D(face, -1, kernel)

        # Save face as separate image
        name = 'extractedID.jpg'
        cv2.imwrite(name, image)

        # Cross-check ID photo with database photo
        image1 = faceEncodings(photo)
        image2 = faceEncodings(name)

        if type(image2) == str:
            print(image2)
            return 0

        else:
            distance = face_recognition.face_distance([image1], image2)
            distance = round(distance[0] * 100)

            # calcuating accuracy level between photos
            accuracy = 100 - round(distance)
            print(f"Photo Similarity Level: {accuracy}%")
            return accuracy

def faceEncodings(imagePath):
    image = face_recognition.load_image_file(imagePath)
    face_enc = face_recognition.face_encodings(image)

    if len(face_enc) == 0:
        return "Face too blurry for recognition!\n"
    else:
        return face_enc[0]

def textExtraction(image):
    # Convert text to grayscale and get text
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    image = cv2.filter2D(image, -1, kernel)

    text = pytesseract.image_to_string(image)
    print(text)

def authenticate(id, image):
    flag = False
    serial = id.data.decode('utf-8')
    if serial in database:
        name = database[serial]["name"]
        age = database[serial]["age"]
        photo = database[serial]["photo"]

        # Print database info from database
        print(f"Information: {name}, {age} years old")
        print(f"ID Number: {serial}")
        print()

        # Check similarity between photos
        similarity = faceDetection(image, photo)
        if similarity > 60:
            flag = True
        else:
            flag = False

        #textExtraction(image)

    else:
        print("ID not found")

    return flag

if __name__ == "__main__":

    # Opens webcam for scanning
    cap = cv2.VideoCapture(0)
    while True:
        # read the frame from the camera
        ret, frame = cap.read()

        # decode detected barcodes & get the image
        # that is drawn
        frame, success = decode(frame)

        # show the image in the window
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == ord("q") or success == True:
            break