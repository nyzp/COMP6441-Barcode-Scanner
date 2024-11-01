# COMP6441-Barcode-Scanner
# Mag's Something Awesome Project

For my Something Awesome project, I wanted to look into ID scanners and break down how they work in terms of authentication. In addition, I wanted to learn how to spot fake IDs and see if I could build something that is able to detect them.

## Description

This program is a simplified ID scanner that reads UNSW ID cards and determines if the ID is valid or not. Upon startup, the webcam starts and waits for an ID card with a barcode to be shown to it for scanning. Upon succession, the program initiates a series of checks:

1. The scanner first reads the barcode and checks if it is the correct type of CODE39.
2. The scanner checks if the ID number matches anyone within the database.
3. The ID photo on the card is captured and compared with the photo saved in the database using facial recognition, and has to achieve a similarity score of at least 60/100.

If the ID passes all three checks, it is considered a valid ID. The program also retrieves information from the database if the card is found and prints it to the terminal.

## Getting Started

### Dependencies

* pyzbar
* numpy
* pytesseract
* PIL
* face_recognition
* cv2
* termcolor
* (that is a lot of libraries, I'm sorry)

### Add Entry to Database
If you would like to add your own ID to receive the "Legitimate ID" result, please find the database at the top of scanner.py and key in your information in the following format:

    "Your UNSW ID card Number Here": {
        "name": "Your Name Here",
        "age": "Your Age Here",
        "zid": "Your zID Here",
        "photo": "photos/your_photo_name.jpg"
    }

Please save a picture of your card's Photo ID in the "Photos" folder, copy the image name and add a "photos/" to the front before pasting that entire string in the "photo" entry as above.

### Executing Program

* Start the program using this command:
```
python3 scanner.py
```
* Hold the ID card up when the webcam window is open. Once the program reads the ID card, the window will close.

*Functions*
```python
# Adds filters to the image captured from webcam for better scanability
imageProcessing(image)

# Scans the barcode found on the card and retrieves its information
decode(image)

# Saves an image of the ID photo and compares it against the database's version
faceDetection(image)

# Calculates face encodings for the specified image
faceEncodings(image)

# Runs the checks on the scanned card
authenticate(id, image)
```


## Help/Issues

* There is an issue with the reader not recognising the photo extracted from the ID card even though it is legitimate. Make sure the card is well-lit and the reader can see it clearly. Try not to make any shaky movements while it is scanning.

## Author

Contributors names and contact info

Magan Leong
z5378443

## Version History

* 0.1
    * Initial Release

## Acknowledgments

Inspiration and References:
* [PyBytes](https://pybit.es/articles/facial-recognition-with-python/)
* StackOverflow