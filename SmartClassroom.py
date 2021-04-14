
import os
import tkinter
from PIL import Image, ImageTk
import cv2
average = 1
fan_on = False
fan_count = 1

#Function Definitions


def attentiveness():
    counter=1
    global average
    #root.destroy()
    #import playsound
    eye_cascPath = 'haarcascade_eye_tree_eyeglasses.xml'  #eye detect model
    face_cascPath = 'haarcascade_frontalface_alt.xml'  #face detect model
    faceCascade = cv2.CascadeClassifier(face_cascPath)
    eyeCascade = cv2.CascadeClassifier(eye_cascPath)
    
    cap = cv2.VideoCapture(0)
    while 1:
        ret, img = cap.read()
        if ret:
            frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Detect faces in the image
            faces = faceCascade.detectMultiScale(
                frame,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                # flags = cv2.CV_HAAR_SCALE_IMAGE
            )
            # print("Found {0} faces!".format(len(faces)))
            if len(faces) > 0:
                # Draw a rectangle around the faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame_tmp = img[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1, :]
                frame = frame[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1]
                eyes = eyeCascade.detectMultiScale(
                    frame,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    # flags = cv2.CV_HAAR_SCALE_IMAGE
                )
                counter+=1
                print('Out of ',len(faces),'Sleeping people are ',len(faces)-(len(eyes)//2))
                percentage = ((len(faces)-(len(eyes)//2))//len(faces))*100
                average+=percentage
                
                
                '''if(len(eyes)<len(faces)/4):
                    playsound
                '''
                frame_tmp = cv2.resize(frame_tmp, (600, 600))
                #, interpolation=cv2.INTER_LINEAR
                cv2.imshow('Face Recognition', frame_tmp)
            waitkey = cv2.waitKey(1)
            if waitkey == ord('q') or waitkey == ord('Q'):
                cv2.destroyAllWindows()
                break
            average = average/counter
            print("thus is average",average)
def submitButtonPressed():
    global fan_on

    user_input = textbox.get()
    print(user_input)
    textbox.delete(0, 'end')
   

    label = user_input
    

    #print ("result: '%s' with %d%% confidence" % (label, confidence))

    if label == 'lamp_on':
        lamp.config(image = lamp_on_pic)
        lamp.image = lamp_on_pic
    elif label == 'lamp_off':
        lamp.config(image = lamp_off_pic)
        lamp.image = lamp_off_pic
    elif label == 'fan_on':
        fan_on = True
    elif label == 'fan_off':
        fan_on = False

def voiceButtonPressed():
    print("Button Pressed")
    print("Feature not yet implemented.")

def attentiveness_real():
    os.system('python detect_blinks.py --shape-predictor shape_predictor_68_face_landmarks.dat')

def fanloop():
    global fan_on
    global fan_count

    if fan_on:
        if fan_count == 1:
            fan_count = 2
            fan.config(image = fan_pic2)
            fan.image = fan_pic2
        elif fan_count == 2:
            fan_count = 3
            fan.config(image = fan_pic3)
            fan.image = fan_pic3
        elif fan_count == 3:
            fan_count = 4
            fan.config(image = fan_pic4)
            fan.image = fan_pic4
        elif fan_count == 4:
            fan_count = 1
            fan.config(image = fan_pic1)
            fan.image = fan_pic1

    root.after(20, fanloop)

#GUI Event Loop Begins
root = tkinter.Tk()
root.title("Smart Classroom")
root.wm_iconbitmap("ML4K-icon.ico")
root.minsize(width = 700, height = 600)
root.maxsize(width = 700, height = 600)

#Load all pictures
load = Image.open("fan-1.png")
load = load.resize((200, 300),Image.ANTIALIAS)
fan_pic1 = ImageTk.PhotoImage(load)

load = Image.open("fan-2.png")
load = load.resize((200, 300),Image.ANTIALIAS)
fan_pic2 = ImageTk.PhotoImage(load)

load = Image.open("fan-3.png")
load = load.resize((200, 300),Image.ANTIALIAS)
fan_pic3 = ImageTk.PhotoImage(load)

load = Image.open("fan-4.png")
load = load.resize((200, 300),Image.ANTIALIAS)
fan_pic4 = ImageTk.PhotoImage(load)

load = Image.open("lamp-off.png")
load = load.resize((400, 300),Image.ANTIALIAS)
lamp_off_pic = ImageTk.PhotoImage(load)

load = Image.open("lamp-on.png")
load = load.resize((400, 300),Image.ANTIALIAS)
lamp_on_pic = ImageTk.PhotoImage(load)

load = Image.open("Circle-icons-mic.png")
load = load.resize((100, 100),Image.ANTIALIAS)
mic_icon = ImageTk.PhotoImage(load)

#Setup GUI Objects
fan = tkinter.Label(root, image = fan_pic1)
fan.image = fan_pic1
fan.grid(row = 0, column = 0)

lamp = tkinter.Label(root, image = lamp_off_pic)
lamp.image = lamp_off_pic
lamp.grid(row = 0, column = 2, sticky = tkinter.S)

shelf = tkinter.Label(root, height = 2, width = 100, bg = "#964B00").grid(row = 1, column = 0, columnspan = 3)

spacer1 = tkinter.Label(root, height = 2).grid(row = 2, column = 0)
spacer2 = tkinter.Label(root, height = 2).grid(row = 5, column = 0)

textbox_frame = tkinter.Frame(root)
textbox_frame.grid(row = 4, column = 0, columnspan = 3)

textbox = tkinter.Entry(textbox_frame, width = 50)
textbox.pack(side = tkinter.LEFT)

submit_text_button = tkinter.Button(textbox_frame, text = "Submit", command = submitButtonPressed).pack(side = tkinter.LEFT)
Attentiveness = tkinter.Button(root, text = "Check Attentiveness", command = attentiveness_real).grid(row = 3, column = 0, columnspan = 2)

output = tkinter.Label(root, text = average,height = 2).grid(row =3,column = 1,columnspan = 1)
voice_button = tkinter.Button(root, text = "Mark Attendance", command = voiceButtonPressed).grid(row = 6, column = 0, columnspan = 3)

root.after(20, fanloop) #Fan Animation

root.mainloop()
