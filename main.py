import csv
import os
from getpass import getpass

import cv2
import numpy as np

import face_recognition


def capture_user_face():
    image_name = input('Please enter your image name: ')
    cam = cv2.VideoCapture(0)
    s, img = cam.read()
    if s:
        cv2.namedWindow("take-picture")
        cv2.imshow("take-picture", img)
        cv2.waitKey(0)
        cv2.destroyWindow("cam-test")
        cv2.imwrite('user_faces/' + image_name + ".jpg", img)


def encode_user_faces():
    user_faces_dir = 'user_faces'
    directory = os.fsencode(user_faces_dir)

    known_face_encodings = []
    known_face_names = []

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".jpg"):
            input_image = face_recognition.load_image_file(user_faces_dir + '/' + filename)
            input_image_encoding = face_recognition.face_encodings(input_image)[0]
            known_face_encodings.append(input_image_encoding)
            known_face_names.append(filename.split('.')[0])
        else:
            continue
    return known_face_encodings, known_face_names


def display_result():
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


def print_authentication_menu():
    print('Please choose one option:')
    print('1. Store image for authentication')
    print('2. Authenticate face')


def print_app_menu():
    print('Please choose one option:')
    print('1. Insert new course')
    print('2. Show all courses')
    print('3. Exit')


print_authentication_menu()

choice = int(input('Your choice: '))

if choice == 1:
    password = getpass('Please enter your password: ')
    if password == 'password':
        capture_user_face()
    else:
        print("You type wrong password")
elif choice == 2:
    video_capture = cv2.VideoCapture(0)

    known_face_encodings, known_face_names = encode_user_faces()

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        display_result()
        cv2.imshow('Video', frame)

        pressedKey = cv2.waitKey(1) & 0xFF
        if pressedKey == ord('q'):
            break
        elif pressedKey == ord('c'):
            video_capture.release()
            cv2.destroyAllWindows()
            if True in matches:
                while True:
                    print_app_menu()
                    app_choice = int(input('Your choice: '))
                    coursesFileName = 'courses.csv'
                    coursesFile = open(coursesFileName)
                    csvReader = csv.reader(coursesFile)
                    if app_choice == 1:
                        courseId = input('Course id: ')
                        courseName = input('Course name: ')
                        fields = [courseId, courseName]
                        with open(coursesFileName, 'a') as f:
                            writer = csv.writer(f)
                            writer.writerow(fields)
                    elif app_choice == 2:
                        print()
                        for row in csvReader:
                            print(row[0] + "\t|" + row[1])
                        print()
                    elif app_choice == 3:
                        break
                break
            elif False in matches:
                print('You do not have permission to use this application')
                break