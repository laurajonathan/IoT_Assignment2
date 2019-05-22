# IoT_Assignment2

This project is intended to create a usable library system which will allow users to create a profile and login. Once this is done users have the options to borrow, search and return books. Users will also have the option to add facial recognition to their system to make logging in easy, use voice recognition to search for books and scan a QR code to return a book. Two raspberry pi's are required for this system to work. This includes all required files needed for the library system.

## Getting Started

The tools for this project are
* [Raspberry Pi + SenseHat](https://au.element14.com/element14/pi3-ibm-iot-learnkit/raspberry-pi-3-ibm-iot-learner/dp/2606882) - The raspberry pi used
* A USB Webcam (for facial recognition and QR scanning)

### Prerequisites

The programming language and library used
```
Python 3.5+
MySQLdb
datetime
os
time
pickle
cv2
imutils
imutils.video
socket
pytz
googleapiclient.discovery
httplib2
oauth2client
pyzbar
re
getpass
passlib
flask
flask_sqlalchemy
flask_marshmallow
mysqlclient
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
oauth2client httplib2
virtualenv
flask_wtf
flask_sqlalchemy
marshmallow-sqlalchemy 
requests
```

The inernal API included
```
flask_api.py
```

### Installing

Install the system modules using apt and pip3

```
For the ease of readability we have provided a
* requirement_master.txt
* requirement_reception.txt

These files will provide all the required steps and information involved in installing libraries and preparing both Raspberry Pi's 
```

### Coding Style

This project is built by following [PEP 8](https://www.python.org/dev/peps/pep-0008/) style and the linting tool used is pylint3

```
pylint3 python_file.py
```

## Structure

### Modules

This project consists of 5 python modules
* facial_recognition.py
* master_main.py
* qr_code_scanner.py
* reception_main.py
*** voice_recognition.py ***

Flask modules (smartlib)
* flask_api.py
* flask_forms.py
* flask_main.py
* flask_site.py

Flask templates/
* login.html
* smartlib.html

Python testing modules
* cloud_database_test.py

## IDE tools

* VScode
* Spyder

## Versioning

Version 1.0

## Authors

* Suwat Tangtragoonviwatt (s3710374)
* Laura Jonathan (s3696013)
* Warren Shipp (s3690682)
* Aidan Afonso (s3660805)

## License

This project is licensed under the RMIT University

## Acknowledgments

* Shekhar Kalra (Project Mentor)
* Matthew Bolger (Project Advisor)
