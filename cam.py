import cv2

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# print (cv2.waitKey.__doc__)
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame)

    c = 42  # cv2.waitKey()
    print(hex(c))
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()

