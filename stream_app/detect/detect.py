import sys
import cv2
import torch

#--- 検出する際のモデルを読込 ---
model = torch.hub.load("stream_app/detect",'yolov5m',source='local')#--- localのyolov5sを使用

#--- 検出の設定 ---
model.conf = 0.5 #--- 検出の下限値（<1）。設定しなければすべて検出
model.classes = [0] #--- 0:person クラスだけ検出する。設定しなければすべて検出
#print(model.names) #--- （参考）クラスの一覧をコンソールに表示


#--- 画像のこの位置より左で検出したら、ヒットとするヒットエリアのためのパラメータ ---
pos_x = 240

def detect(imgs):
    #--- 推定の検出結果を取得 ---
    results = model(imgs, size=160) #--- 320ピクセルの画像にして処理

    #--- 出力 ---
    #--- 検出結果を画像に描画して表示 ---
    #--- 各検出について

    person_conf = 0
    for *box, conf, cls in results.xyxy[0]:  # xyxy, confidence, class

        #--- クラス名と信頼度を文字列変数に代入
        s = model.names[int(cls)]+":"+'{:.1f}'.format(float(conf)*100)

        if model.names[int(cls)] == "person":
            person_conf = float(conf)

        #--- ヒットしたかどうかで枠色（cc）と文字色（cc2）の指定
        if int(box[0])>pos_x :
            cc = (255,255,0)
            cc2 = (128,0,0)
        else:
            cc = (0,255,255)
            cc2 = (0,128,128)

        #--- 枠描画
        cv2.rectangle(
            imgs,
            (int(box[0]), int(box[1])),
            (int(box[2]), int(box[3])),
            color=cc,
            thickness=2,
            )
        #--- 文字枠と文字列描画
        cv2.rectangle(imgs, (int(box[0]), int(box[1])-20), (int(box[0])+len(s)*10, int(box[1])), cc, -1)
        cv2.putText(imgs, s, (int(box[0]), int(box[1])-5), cv2.FONT_HERSHEY_PLAIN, 1, cc2, 1, cv2.LINE_AA)

    return person_conf, imgs