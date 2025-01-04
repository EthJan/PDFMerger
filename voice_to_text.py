import speech_recognition as sr
import pyttsx3
import os

# Initialize the voice recognizer object (interacts and interprets mic input)
recognizer = sr.Recognizer()
# Dictionary for spoken phrases to corresponding characters
mappings = {
    # Special Characters
    "leftbracket": "(",
    "rightbracket": ")",
    "leftbrace": "{",
    "leftcurlybracket": "{",
    "rightbrace": "}",
    "rightcurlybrace": "}",
    "comma": ",",
    "period": ".",
    "dot": ".",
    "period": ".",
    "semicolon": ";",
    "colon": ":",
    "exclamation": "!",
    "questionmark": "?",
    "hyphen": "-",
    "dash": "-",
    "underscore": "_",
    "plus": "+",
    "minus": "-",
    "equals": "=",
    "asterisk": "*",
    "slash": "/",
    "backslash": "\\",
    "pipe": "|",
    "tilde": "~",
    "caret": "^",
    "percent": "%",
    "dollar": "$",
    "at": "@",
    "hash": "#",
    "ampersand": "&",
    "openquote": "\"",
    "closequote": "\"",
    "singlequote": "'",
    "backtick": "`",
    "lessthan": "<",
    "greaterthan": ">",
    "equalsign": "=",

    # Capital Letters
    "capitala": "A",
    "capitalb": "B",
    "capitalc": "C",
    "capitald": "D",
    "capitale": "E",
    "capitalf": "F",
    "capitalg": "G",
    "capitalh": "H",
    "capitali": "I",
    "capitalj": "J",
    "capitalk": "K",
    "capitall": "L",
    "capitalm": "M",
    "capitaln": "N",
    "capitalo": "O",
    "capitalp": "P",
    "capitalq": "Q",
    "capitalr": "R",
    "capitals": "S",
    "capitalt": "T",
    "capitalu": "U",
    "capitalv": "V",
    "capitalw": "W",
    "capitalx": "X",
    "capitaly": "Y",
    "capitalz": "Z",

    # Other
    "newline": "\n",
}


def record():
    while(1):
        try:
            # Take input from mic as source
            with sr.Microphone() as source2:
                # Let recognizer know about ambient noise
                recognizer.adjust_for_ambient_noise(source2, duration=0.1)

                 # Listen for user input
                audio2 = recognizer.listen(source2)
                
                # Try to figure out the audio using Google
                inputText = recognizer.recognize_google(audio2, language="en-US").lower()

                # print("This is the recorded text: " + inputText)

                # Replace spoken phrases with corresponding special characters and capital letters
                for key, value in mappings.items():
                    special_text = inputText.replace(key, value)
    
                # Remove unwanted spaces to prevent seperation of letters and numbers
                converted_text = special_text.replace(" ", "")

                # print("This is the text after editing: " + converted_text)

                # Replace space keyword with a space
                converted_text = converted_text.replace("space"," ")

                # print("This is the text being converted: " + converted_text)


                return converted_text
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("No Sound Detected")
        

def convert(text):
    f = open(output_directory, "a")
    f.write(text)
    print(text)
    f.close
    # Print to an output file that we can later read

def voice_input():
    print("Start speaking, seperating files with a 'space'. Say 'stop' to stop.")
    actual_text = ""
    while (1):
        text = record()
        if text in ["stop"]:
            print("Ending program.")
            exit()
        # Proceed only when text is not empty
        elif text in ["enter"]:
            print("Converting " + actual_text)
            convert(actual_text)
            actual_text = ""
        elif text in ["clear"]:
            print("Reset current entry")
            actual_text = ""
        else:
            actual_text +=  text
            print("Total text so far:  " + actual_text)
    print("Conversion completed")

# Create a new output file (auto handle errors)
current_directory = os.path.dirname(os.path.abspath(__file__))
output_directory =  os.path.join(current_directory, "output.txt")
with open(output_directory, "w") as f:
    pass

if __name__ == "__main__":  
    voice_input()
    f.close

