
import cv2
import csv
import numpy as np
from matplotlib import image
from sklearn.cluster import KMeans
from collections import Counter
import time
import picamera
import picamera.array
import RPi.GPIO as GPIO
from time import sleep
import datetime
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)
GPIO.setup(8,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
#sutakkuカウンター
count = 0
#ピン指定
right_front=8
left_front=24
right_back=25
left_back=23



###############################
#重心関数
def detect_red_color(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

     # 赤色のHSVの値域1
    hsv_min = np.array([0,130,140])
    hsv_max = np.array([0, 255, 255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)
    result1 = cv2.bitwise_and(img,img, mask = mask1)

    # 赤色のHSVの値域2
    hsv_min = np.array([175,50,20])
    hsv_max = np.array([179, 255, 255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)
    result2 = cv2.bitwise_and(img,img, mask = mask2)
    
    
    picture = result1|result2
    
    grayming = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
    ret_0, binary_img = cv2.threshold(grayming,10,255,cv2.THRESH_BINARY)
    

    return ret_0, binary_img

######################################
#方向指定
def forward(x=0):
    GPIO.output(right_front,GPIO.HIGH)
    GPIO.output(left_front,GPIO.HIGH)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.LOW)
    sleep(x)
    return()

def back(x=0):
    GPIO.output(right_back,GPIO.GPIO.HIGH)
    GPIO.output(left_back,GPIO.GPIO.HIGH)
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.LOW)
    sleep(x)
    return()

def leftturn(x=0):
    GPIO.output(right_front,GPIO.HIGH)
    GPIO.output(left_front,GPIO.LOW)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.HIGH)
    sleep(x)
    return()

def rightturn(x=0):
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.HIGH)
    GPIO.output(right_back,GPIO.HIGH)
    GPIO.output(left_back,GPIO.LOW)
    sleep(x)
    return()

def leftfacing(x=0):#右タイヤ前進,左タイヤストップ
    GPIO.output(right_front,GPIO.HIGH)
    GPIO.output(left_front,GPIO.LOW)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.LOW)
    sleep(x)
    return()    

def rightfacing(x=0): #右タイヤストップ,左タイヤ前進
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.HIGH)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.LOW)
    sleep(x)
    return()

def stop(x):
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.LOW)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.LOW)
    sleep(x)
    return()
   
####################################

while True: 
    #画像読み込み

    fn ="img_noML.jpg"
    dt_now = datetime.datetime.now()
    
    with picamera.PiCamera() as camera:
        camera.resolution = (600,800)
        time.sleep(0.1)
        camera.capture(fn)
        
    dt_now = datetime.datetime.now()
    start_time = time.perf_counter()
    sleep(1)
 #stop time
    t_stop = 0.1
    t_turn = 0.1
    K = 4 #4色に分ける; 分割後のグループの数


    img = cv2.imread(fn)
    # 画像をそのままk-meansにかけることはできないので、shapeを(ピクセル数, 3(BGR))に変換
    Z = img.reshape((-1, 3))
    # np.float32型に変換
    Z = np.float32(Z)
    # k-meansの終了条件
    # デフォルト値を使用
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 8, 1.0)
    # k-means処理
    _, label, center = cv2.kmeans(
        Z, K, None, criteria, 8, cv2.KMEANS_RANDOM_CENTERS)

    # np.uint8型に変換
    center = np.uint8(center)
    # グループごとにグループ内平均値を割り当て
    res = center[label.flatten()]
    # 元の画像サイズにもどす
    res2 = res.reshape((img.shape))

    # 画像の保存
    name_1 = dt_now.strftime('%H_%M_%S_') + "kmeans"
    cv2.imwrite(name_1 + ".jpg", res2)

    red_mask = detect_red_color(res2)
    mu = cv2.moments(red_mask[1]) #red_mask[1] = binary_img

    pixel_number = np.size(red_mask[1])  # 全ピクセル数
    pixel_sum = np.sum(red_mask[1])  # 輝度の合計数
    white_pixel_number = pixel_sum/255  # 白のピクセルの数
    occupation = white_pixel_number/pixel_number
    print(occupation)
    
    x = 0
    y = 0

    if occupation<0.05:

        if mu["m00"]!=0:
            x = int(mu["m10"]/mu["m00"])
            y = int(mu["m01"]/mu["m00"])
            print(x,y)
            cv2.circle(res2, (x,y), 30, color=(255, 0, 0), thickness=3, lineType=cv2.LINE_4, shift=0)
            name_2 = dt_now.strftime('%H_%M_%S_') + "moment"
            cv2.imwrite(name_2 + '.jpg', res2)

            if x<128:
                print("move to left")
                leftturn(t_turn)
                stop(t_stop)
                count = 0

            elif x>700:
                print("move to right")
                rightturn(t_turn)
                stop(t_stop)
                count = 0

            else:
                print("PERFECT! move forward")
                forward(2)
                stop(t_stop)
                count = 0

        else:
            print("just move forward")
            forward(2)
            stop(t_stop)
            count = count + 1

        if count > 200:
            print("too much movement...")
            leftfacing(t_turn)
            stop(t_stop)
            count = 0

    else:
        print("CLOSE ENOUGH :)")
        stop(t_stop)


    cv2.destroyAllWindows()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(elapsed_time)
    dt_now = datetime.datetime.now()
    with open('img_data.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        list = [dt_now.strftime('%H:%M:%S'), '{:.05f}'.format(occupation), str(x),str(y),'{:.02f}'.format(elapsed_time)]
        writer.writerow(list)
    
GPIO.cleanup()
