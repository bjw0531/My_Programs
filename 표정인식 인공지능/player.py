import cv2
import timeit
import time
import tensorflow as tf
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow import keras


# 영상 검출기
def videoRecorder(cam, cascade):
    len_crop_images = 0
    # neutral = 1
    # happy = 2
    # sad = 3
    # angry = 4
    mode = 1
    modename = ["", "dsleepy", "happy", "sad", "angry"]
    while True:
        start_t = timeit.default_timer()

        # 캡처 이미지 불러오기
        ret, img = cam.read()
        # 영상 압축
        # img = cv2.resize(img, dsize=None, fx=1.0, fy=1.0)
        # 그레이 스케일 변환
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cascade 얼굴 탐지 알고리즘
        results = cascade.detectMultiScale(gray, 1.3, 5)  # 입력 이미지

        crop_images = []
        for box in results:
            x, y, w, h = box
            crop = img[y : y + h, x : x + w]
            resize = cv2.resize(crop, (192, 192))
            crop_images.append(resize)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), thickness=2)

        terminate_t = timeit.default_timer()
        FPS = "fps" + str(int(1.0 / (terminate_t - start_t)))

        # 텍스트 출력
        cv2.putText(img, FPS, (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 1)
        cv2.putText(
            img, modename[mode], (30, 60), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 1
        )

        # 영상 출력

        cv2.imshow("facenet", img)
        for i in range(len(crop_images)):
            cv2.imshow(str(i), crop_images[i])

        if len(crop_images) < len_crop_images:
            for i in range(len(crop_images), len_crop_images):
                cv2.destroyWindow(str(i))

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        if ord("1") <= key and key <= ord("4"):
            mode = int(chr(key))
        if key == ord(' '):
            for i in range(len(crop_images)):
                directory = 'train_data/' + modename[mode] + "/" + str(time.time()).replace('.','-') + ".jpg"
                cv2.imwrite(directory, crop_images[i])
                print("image saved",directory)

        len_crop_images = len(crop_images)

imsize = 192
def videoDetector(cam, cascade, model):
    mode = 1
    modename = ["angry", "dsleepy", "happy", "sad"]
    while True:
        start_t = timeit.default_timer()

        # 캡처 이미지 불러오기
        ret, img = cam.read()
        # 영상 압축
        # img = cv2.resize(img, dsize=None, fx=1.0, fy=1.0)
        # 그레이 스케일 변환
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cascade 얼굴 탐지 알고리즘
        results = cascade.detectMultiScale(gray, 1.3, 5)  # 입력 이미지

        crop_images = []
        for box in results:
            x, y, w, h = box
            crop = img[y : y + h, x : x + w]
            resize = cv2.resize(crop, (imsize, imsize))
            crop_images.append(resize)
            
            img_arr = tf.keras.utils.img_to_array(resize)
            img_arr = np.array([img_arr])
            k = model.predict(img_arr)
            print(np.argmax(k), modename[np.argmax(k)], k)
            cv2.putText(img, modename[np.argmax(k)], (x, y), cv2.FONT_HERSHEY_DUPLEX, 2, (0,255,0),2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)

        terminate_t = timeit.default_timer()
        FPS = "fps" + str(int(1.0 / (terminate_t - start_t)))

        # 텍스트 출력
        cv2.putText(img, FPS, (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 1)

        # 영상 출력
        cv2.imshow("facenet", img)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break


cascade_filename = "haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(cascade_filename)
cam = cv2.VideoCapture(0)
model = keras.models.load_model('./my_camera_model192_dataug2.h5')



videoDetector(cam,cascade, model)
#videoRecorder(cam, cascade)