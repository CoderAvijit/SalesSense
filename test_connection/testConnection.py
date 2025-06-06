import speech_recognition as sr

def takeCommand():
    r = sr.Recognizer()

    try:
        mic_index = 16  # Try 6, 12, or 16 if needed
        print(f"Initializing microphone... {mic_index}")
        with sr.Microphone(device_index=mic_index) as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print("User said:\n", query)
            return query

        except sr.UnknownValueError:
            print("Could not understand the audio. Please try again.")
            return None

        except sr.RequestError as e:
            print("Could not request results. Error:", e)
            return None

    except Exception as e:
        print("Microphone error:", e)
        return None

if __name__ == "__main__":
    result = takeCommand()
    if result:
        print("Microphone input test completed.")
    else:
        print("No valid input detected.")
