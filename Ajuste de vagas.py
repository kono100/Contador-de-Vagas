import cv2
import pickle
import os

rectW, rectH = 107, 48

try:
    with open('carParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + rectW and y1 < y < y1 + rectH:
                posList.pop(i)
    with open('carParkPos', 'wb') as f:
        pickle.dump(posList, f)

file_path = "carPark.mp4"  

if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
    is_image = True
    cap = cv2.imread(file_path)
else:
    is_image = False
    cap = cv2.VideoCapture(file_path)

while True:
    if not is_image:
        ret, frame = cap.read()
        if not ret:
            break
    else:
        frame = cap.copy()

    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    for pos in posList:
        cv2.rectangle(frame, pos, (pos[0] + rectW, pos[1] + rectH), (0, 0, 255), 2)

    cv2.imshow("Image", frame)
    cv2.setMouseCallback("Image", mouseClick)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

if not is_image:
    cap.release()

cv2.destroyAllWindows()
