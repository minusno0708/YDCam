import time
import datetime

import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views import View

from stream_app.detect.detect import detect
from stream_app.record import record_capture

from .models import Record

# ストリーミング映像を表示するview
class IndexView(View):
    def get(self, request):
        return render(request, 'stream_app/index.html', {})

# ストリーミング画像を定期的に返却するview
def video_feed_view():
    video = generate_frame()
    return lambda _: StreamingHttpResponse(video, content_type='multipart/x-mixed-replace; boundary=frame')


# フレーム生成・返却する処理
def generate_frame():
    capture = cv2.VideoCapture(0)  # USBカメラから

    while True:
        if not capture.isOpened():
            print("Capture is not opened.")
            break
        # カメラからフレーム画像を取得
        ret, frame = capture.read()
        if not ret:
            print("Failed to read frame.")
            break

        # フレーム画像を物体検知し、存在確率と処理後の画像を取得
        conf, frame = detect(frame)
        # 画像に時間を添付
        frame = set_time(frame)

        # フレーム画像バイナリに変換
        ret, jpeg = cv2.imencode('.jpg', frame)
        byte_frame = jpeg.tobytes()

        # 人間を検知した場合DBに記録する
        if conf > 0.75:
            record_capture(conf, byte_frame)

        # フレーム画像のバイナリデータをユーザーに送付する
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
        
        time.sleep(0.2)
    capture.release()

# 画像に時刻を添付する処理
def set_time(frame):
    dt_now = datetime.datetime.now()
    now = dt_now.strftime("%Y/%m/%d %H:%M:%S")
    cv2.putText(frame, now, (0, 15), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1, cv2.LINE_AA)

    return frame

# 保存した画像を表示するview
def record_view(request):
    records = Record.objects.all()
    context = {'records': records}
    return render(request, 'stream_app/record.html', context)