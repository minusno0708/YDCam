import sys
import cv2

from detect import detect

#--- 映像の読込元指定 ---
#camera = cv2.VideoCapture("../pytorch_yolov3/data/sample.avi")#--- localの動画ファイルを指定
camera = cv2.VideoCapture(0)                #--- カメラ：Ch.(ここでは0)を指定

def main():
    while True:

        #--- 画像の取得 ---
        #  imgs = 'https://ultralytics.com/images/bus.jpg'#--- webのイメージファイルを画像として取得
        #  imgs = ["../pytorch_yolov3/data/dog.png"] #--- localのイメージファイルを画像として取得
        ret, imgs = camera.read()              #--- 映像から１フレームを画像として取得

        imgs = detect(imgs)

        #--- 描画した画像を表示
        cv2.imshow('detect',imgs)

        #--- 「q」キー操作があればwhileループを抜ける ---
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()