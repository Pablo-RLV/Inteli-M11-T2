import cv2
import requests
import numpy as np
import fastapi
import io

app = fastapi.FastAPI()
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
url = "http://10.128.0.104/image"

def download_image():
    response = requests.get(url)
    img = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
    return img

def detect_faces(img):
    faces = face_cascade.detectMultiScale(img, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return img

@app.get('/')
def image():
    img = download_image()
    img_with_faces = detect_faces(img)
    _, img_encoded = cv2.imencode('.jpg', img_with_faces)
    return fastapi.responses.StreamingResponse(io.BytesIO(img_encoded.tobytes()), media_type='image/jpeg')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)