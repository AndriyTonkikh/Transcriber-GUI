# Transcriber-GUI
This is a desktop application that allows users to transcribe audio or video files to text using Python. The user interface is built using the PyQt6 library.
Requirements

The following libraries are required to run this application:

    PyQt6
    pydub
    speech_recognition

Installation

    Clone this repository to your local machine.
    Install the required libraries using pip:
    
    pip install PyQt6 pydub SpeechRecognition


    Run the application by executing the transcriber.py file.

Usage

    Click the "Open file" button to select a media file in mp3, mp4, avi, or wmv format.
    Choose the language for transcription from the drop-down menu (UA - Ukrainian, ENG - English, ru - Russian).
    Click the "Transcribe" button to begin transcription. The progress will be displayed in the progress bar.
    Once the transcription is complete, the text will be displayed in the text box.
    Click the "Save txt" button to save the transcription to a text file.
    Click the "Save wav" button to save the audio to a wav file.
    Click the "Clear" button to clear the text box.

License

This application is released under the MIT License.
