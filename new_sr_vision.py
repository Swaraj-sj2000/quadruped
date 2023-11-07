import cv2
import threading
import numpy as np
import pyttsx3
import multiprocessing
import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

command = -1

def listenMic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en_in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Say that again, please.")
        return ""
    except sr.RequestError:
        print("Could not request results from Speech Recognition service.")
        return ""
    return query.lower()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def open_camera():
    speak("opening camera")
    cap = cv2.VideoCapture(0)
    while True:
        isTrue, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame=cv2.flip(frame,1)
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        detector=cv2.CascadeClassifier("haar_face.xml")
        face_rect=detector.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=3)
        for (x,y,w,h) in face_rect:
            if(len(face_rect)>1):
                r=(0,0,255)
            else:r=(0,255,0)
            cen=(np.intc(int(x)+int(w)/2),np.intc(int(y)+int(h)/2))
            rad=np.intc(int(h)/2+int(w)/2-47)
            cv2.circle(frame,cen,rad,r,thickness=1)
            tx=int(x)+int(w)/2-20
            ty=int(y)-20
            cv2.putText(frame,"Face detected ",(np.intc(tx),np.intc(ty)),cv2.FONT_HERSHEY_TRIPLEX,0.3,(255,0,0),thickness=1)
        cv2.imshow("video", frame)
        if cv2.waitKey(1) & 0XFF == ord('x'):
            break
    cap.release()
    cv2.destroyAllWindows()

def main():
    while True:
        query = listenMic()
        if query == "":
            continue
        if "quit" in query:
            speak("okay bye")
            break
        elif "open camera" in query:
            process = multiprocessing.Process(target=open_camera)
            process.start()
        elif "stop camera" in query:
            process.terminate()


if __name__ == "__main__":
    
    main()
    
