import cv2

from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse

from .record import record_capture

# Create your views here.
def index(request):
    return HttpResponse("<img src='/video_feed'/>")

def video_feed_view():
    video = generate_frame()
    return lambda _: StreamingHttpResponse(video, content_type='multipart/x-mixed-replace; boundary=frame')

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

        # フレーム画像バイナリに変換
        ret, jpeg = cv2.imencode('.jpg', frame)
        byte_frame = jpeg.tobytes()

        record_capture(byte_frame)

        # フレーム画像のバイナリデータをユーザーに送付する
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')

    capture.release()