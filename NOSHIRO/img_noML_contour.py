#以下自作ライブラリ
import MPU2
import bmp2

#別からもらったもの
import math
import geopy
from geopy.distance import geodesic
from time import sleep
from gps3 import gps3
import csv
import datetime 
import cv2
import numpy as np
import picamera
import picamera.array
import RPi.GPIO as GPIO
import time 


#################

#モーターの設定とタイヤの回し方
right_front=10
left_front=24
right_back=9
left_back=23
##############
#GPSRUN用のsetup
#ゴールの緯度経度
goal_lat = ??
goal_lon = ??
goal_latr = math.radians(goal_lat)
goal_lonr = math.radians(goal_lon)
count = 0

#変更可能GPSRUN
#タイヤを何秒間回すか
tt = 2    #直進、後進に関する秒数
tf = 0.4  #右or左向き、右左回転に関する秒数
#変更可能画像処理
t_stop = 0.1 #stop time
t_turn = 0.3 #turn time
t_forward = 1 #forward time


GPIO.setmode(GPIO.BCM)  #GPIOの番号で指定する

GPIO.setup(right_front,GPIO.OUT) #right_frontのピンを出力端子として初期値0で使用する
GPIO.setup(left_front,GPIO.OUT)
GPIO.setup(right_back,GPIO.OUT)
GPIO.setup(left_back,GPIO.OUT)

GPIO.setwarnings(False) #GPIOピンの値がデフォルトでない時に出てくる文

########################################
def stop(x):
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.LOW)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.LOW)
    sleep(x)
    return()

def forward(x):
    GPIO.output(right_front,GPIO.HIGH)
    GPIO.output(left_front,GPIO.HIGH)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.LOW)
    sleep(x)
    return()

def back(x):
    GPIO.output(right_back,GPIO.HIGH)
    GPIO.output(left_back,GPIO.HIGH)
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.LOW)
    sleep(x)
    return()

def leftturn(x):
    GPIO.output(right_front,GPIO.HIGH)
    GPIO.output(left_front,GPIO.LOW)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.HIGH)
    sleep(x)
    return()

def rightturn(x):
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.HIGH)
    GPIO.output(right_back,GPIO.HIGH)
    GPIO.output(left_back,GPIO.LOW)
    sleep(x)
    return()

def leftfacing(x):#右タイヤ前進,左タイヤストップ
    GPIO.output(right_front,GPIO.HIGH)
    GPIO.output(left_front,GPIO.LOW)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.LOW)
    sleep(x)
    return()    

def rightfacing(x): #右タイヤストップ,左タイヤ前進
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.HIGH)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.LOW)
    sleep(x)
    return()


###############################
#スタック処理
def stack(x,y,z): #x=モーター動かす秒数, y=動きごとに何秒止まるか
    global count
    back(0.3)
    stop(1)
    back(0.3) 
    stop(1)
    back(0.3)
    stop(1)
    forward(1)
    
    magnet = mpu9250.readMagnet()
    mz = magnet[2]
    z = 0    
    while True:
      magnet = mpu9250.readMagnet()
      mz = magnet[2]
      if mz < 0:
         print('change')
         if z %2 == 1:
             forward(5)
             stop(0.5)             
         else:
             back(5)
             stop(0.5)
             z += 1
      else:
            break
    forward(0.5)        
    #スタック処理 
    while True:
      Accel = mpu9250.readAccel()
      ax = Accel['x']
      ay = Accel['y']
      if -0.1<=ax<=0.1 and -0.1<=ay<=0.1:
          stop(1)
          if count%4 ==0:
             back(0.8)
             stop(0.5)
             leftturn(y)
             print('s_leftturn')
             stop(1)
          elif count%4 == 1:
             back(0.8)
             stop(0.5)
             rightturn(y)
             print('s_rightturn')
             stop(1)
          elif count%4 == 2:
             rightturn(y)
             print('s_rightturn*2')
             stop(1)
             rightturn(y)
             stop(1)
          elif count%4 == 3:
             leftturn(y)
             print('s_leftturn*2')
             stop(1)
             leftturn(y)
             stop(1)
          #向きを変えたら前進
          forward(1)  
          count += 1
      else:
         stop(1)
         print('escape stack')
         break
         #forward(tt)
     
      
def rad_magnet(mx2, my2):
    rad = 0
    rad = math.atan2(mx2, my2)
    return rad

def Deg_cansat(mx2,my2):
    deg_cansat = rad_magnet(mx2,my2)*180/math.pi    
    if deg_cansat<0:
       return(deg_cansat+ 360)
    else:
       return(deg_cansat)
       
def Deg_goal(deg_goal):
   if deg_goal<0:
     return(deg_goal+ 360)
   else:
     return(deg_goal)
  
########
#カメラ判定setup
#重心関数
def detect_red_color(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 赤色のHSVの値域1
    #変更可能
    #hsv_min = np.array([0, 100,20]) #赤範囲広め
    #hsv_min = np.array([0,104,84]) #中間くらい 
    #hsv_min = np.array([0,200,50]) #赤範囲超狭め
    #hsv_min = np.array([0,130,140]) #赤範囲狭め
    #hsv_max = np.array([10, 255, 255])
    hsv_min = np.array([0,175,130]) #赤範囲超超狭め
    hsv_max = np.array([0,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)
    result1 = cv2.bitwise_and(img,img, mask = mask1)

    # 赤色のHSVの値域2
    #変更可能
    hsv_min = np.array([160, 100, 20]) #マスク範囲中間くらい 
    #hsv_min = np.array([150,64,0]) #マスク範囲広め
    #hsv_min = np.array([150,200,50])  #マスク範囲超狭め
    #hsv_min = np.array([175,50,20])  #マスク範囲狭め
    hsv_max = np.array([179,255,255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)
    result2 = cv2.bitwise_and(img,img, mask = mask2)
    
    
    picture = result1|result2
    
    grayming = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
    ret_0, binary_img = cv2.threshold(grayming,10,255,cv2.THRESH_BINARY)
    cv2.imwrite("gps2img_binary.jpg", binary_img)
    

    return ret_0, binary_img


####################################
#制御履歴設定
        
with open("st_noML_contour.csv", mode = "w") as f:
    writer = csv.writer(f)

with open("st_noML_contour.csv", mode="r+") as f: 
    f.truncate(0)  

with open("st_noML_contour.csv", mode = "w") as f:
    writer = csv.writer(f)
    writer.writerow(['TIME (JST)', 'occupation', 'x-cord.', 'y-cord.', 'process time', 'comment', 'stack comment', "elapsed time"])
####################################

while True:
    #画像読み込み
    fn ="st_noML_contour.jpg"
    comments = ""
    stack_comment = ""

    #9軸センサの加速度と地磁気取得
    mpu9250 = MPU2.MPU9250()
    Accel = mpu9250.readAccel()
    magnet = mpu9250.readMagnet()
    
    with picamera.PiCamera() as camera:
        camera.resolution = (600,800)
        time.sleep(0.1)
        camera.capture(fn)
    
    dt_now = datetime.datetime.now()
    start_time = time.perf_counter()
    sleep(1)

    pic_name="cone.jpg"
    pic_name_out="coneout.jpg"
    gray_pic="conegray.jpg"


    img = cv2.imread(fn, cv2.IMREAD_COLOR)
    red_mask = detect_red_color(img)

    #読み込んだ画像の重心、輪郭を取得
    contours, hierarchy = cv2.findContours(red_mask[1], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 255, 0), 2, cv2.LINE_AA)
    
    mu = cv2.moments(red_mask[1], False)
    
    pixel_number = np.size(red_mask[1])  # 全ピクセル数
    pixel_sum = np.sum(red_mask[1])  # 輝度の合計数
    white_pixel_number = pixel_sum/255  # 白のピクセルの数
    occupation = white_pixel_number/pixel_number
    print(occupation)
    
    x = 0
    y = 0

    Accel = mpu9250.readAccel()
    ax = Accel['x']
    ay = Accel['y']

    if occupation<0.2: #変更可能
        print("get closer...")
        if mu["m00"]!=0:
            x = int(mu["m10"]/mu["m00"])
            y = int(mu["m01"]/mu["m00"])
            print(x,y)
            cv2.circle(img, (x,y), 30, color=(255, 0, 0), thickness=3, lineType=cv2.LINE_4, shift=0)
            cv2.imwrite('st_noML_contour_moment.jpg', img)
            
            if occupation > 0.01 and occupation  < 0.03:
                print("too far")
                comments = "too far"
                forward(t_forward)
                if -0.1<=ax<=0.1 and -0.1<=ay<=0.1:
                    stop(1)
                    stack(1,0.1,1)
                    print('stack')
                    comments_stack = "スタック処理開始" 
                    
                else:
                    stop(t_stop)
                    count = 0
            
            if x<150:
                print("move to left")
                comments = "move to left"
                leftturn(t_turn)
                if -0.1<=ax<=0.1 and -0.1<=ay<=0.1:
                    stop(1)
                    stack(1,0.1,1)
                    print('stack')
                    comments_stack = "スタック処理開始" 
                    
                else:
                    stop(t_stop)
                    count = 0
        

            elif x>400:
                print("move to right")
                comments = "move to right"
                rightturn(t_turn)
                if -0.1<=ax<=0.1 and -0.1<=ay<=0.1:
                    stop(1)
                    stack(1,0.1,1)
                    print('stack')
                    comments_stack = "スタック処理開始" 
                    
                else:
                    stop(t_stop)
                    count = 0

            else:
                print("PERFECT! move forward")
                comments = "PERFECT! move forward"
                forward(t_forward)
                if -0.1<=ax<=0.1 and -0.1<=ay<=0.1:
                    stop(1)
                    stack(1,0.1,1)
                    print('stack')
                    comments_stack = "スタック処理開始"
                     
                else:
                    stop(t_stop)
                    count = 0

        else:
            print(x,y)
            print("no red detected")
            comments = "PERFECT! move forward"
            leftfacing(t_turn)
            if -0.1<=ax<=0.1 and -0.1<=ay<=0.1:
                    stop(1)
                    stack(1,0.1,1)
                    print('stack')
                    comments_stack = "スタック処理開始" 
                    
            else:
                stop(t_stop)
                count = count + 1

        if count > 200:
            print("too much movement...")
            comments = "too much movement..."
            leftfacing(t_turn)
            if -0.1<=ax<=0.1 and -0.1<=ay<=0.1:
                    stop(1)
                    stack(1,0.1,1)
                    print('stack')
                    comments_stack = "スタック処理開始" 
                    
            else:
                stop(t_stop)
                count = 0
    else:
        if mu["m00"]!=0:
            x = int(mu["m10"]/mu["m00"])
            y = int(mu["m01"]/mu["m00"])
            print(x,y)
            cv2.circle(img, (x,y), 30, color=(255, 0, 0), thickness=3, lineType=cv2.LINE_4, shift=0)
            cv2.imwrite('contour_noML_moment.jpg', img)
        print("GOAL!!")
        comments = "GOAL!!"
        stop(t_stop)


    cv2.destroyAllWindows()

    #制御履歴
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    with open('st_noML_contour.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        list = [dt_now.strftime('%H:%M:%S'), '{:.05f}'.format(occupation), str(x),str(y), comments, stack_comment, '{:.02f}'.format(elapsed_time)]
        writer.writerow(list)


    if comments == "GOAL!!":
        break

      

    
GPIO.cleanup()
