"""
voice_recognition.py

Modified by Suwat Tangtragoonviwatt (s3710374)
            Laura Jonathan (s3696013)
            Warren Shipp (s3690682)
            Aidan Afonso (s3660805)


The VoiceRecognition class listens to audio from
the designated microphone and returns a string.

"""

import speech_recognition as sr
import util

class VoiceRecognition():
    """
    Voice Recognition class
    Listen to audio input and detect speech.
    """
    def __init__(self):
        #set microphone name and find its device id
        MIC_NAME = "Plantronics GameCom 780/788: USB Audio (hw:1,0)"
        with util.noalsaerr():
            for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
                if(microphone_name == MIC_NAME):
                    self.device_id = i
                    break
        self.r = sr.Recognizer()
    def listen(self):
        """
        Begin listening to audio input and return recognised text and any errors
        """
        error = 0
        result = ""
        #listen for audio
        with util.noalsaerr(), sr.Microphone(device_index = self.device_id) as source:
            self.r.adjust_for_ambient_noise(source)
            print("Listening...")
            try:
                audio = self.r.listen(source, timeout = 1.5)
            except sr.WaitTimeoutError:
                error = 1

        # recognize speech using Google Speech Recognition
        try:
            result = self.r.recognize_google(audio)
        except sr.UnknownValueError:
            error = 2
        except sr.RequestError as e:
            error = 3
            result = e
        finally:
            return error, result
