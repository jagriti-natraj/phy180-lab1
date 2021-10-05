import cv2
import time
import math
import matplotlib.pyplot as plt 

cap = cv2.VideoCapture('IMG_3159_Trim_1.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
total = cap.get(cv2.CAP_PROP_FRAME_COUNT)
count = 0
X = []
Y = []
theta_list = []
t = []
frame_list = []
delta_time = []
delta_theta = []
cum_time = 0
print("Extracting centroids from video source...")

while cap.isOpened():
    ret,frame = cap.read()
    # cv2.imshow('window-name',NoneType frame)
    # cv2.imwrite("frame%d.jpg" % count, frame)

    if count <= 10:
        count += 1
        continue

    # cv2.imshow("lmao", frame)
    # cv2.waitKey(0)

    if isinstance(frame, type(None)):
        break
    width, height, something = frame.shape

    # print("Cropping by y:", 3*height//5, "x: ", width//5)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)[3*height//5:, width//5:]
    gray = cv2.GaussianBlur(gray, (41, 41), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

    if maxLoc[0] > 0 and maxLoc[1] > 0:
        x = -649 + 214 + maxLoc[0]
        y = -139 + 646 + maxLoc[1]
        percentage_delta_x = 40/maxLoc[0]
        percentage_delta_y = 40/maxLoc[1]
        theta = math.atan(x/y)
        if theta > 0.46: 
            continue
        X.append(x)
        Y.append(y)
        theta_list.append(theta)
        delta_theta.append(theta*(percentage_delta_x + percentage_delta_y))
        t.append(cum_time)
        delta_time.append(1/(fps * 2))
        frame_list.append(count)
    cum_time += 1/fps
    cv2.circle(gray, maxLoc, 5, (255, 0, 0), 2)
    cv2.imshow("Naive", gray)
    cv2.waitKey(0)

    if count % 100 == 0:
        print(f"{round(count*100/total, 2)}% done.")

    # time.sleep(1)
    count = count + 1
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
print("Done!")

with open('processed_data.txt', 'w') as file:
    for (x, y, a, b) in zip(t, theta_list, delta_time, delta_theta):
        file.write(f"{x} {y} {a} {b}\n")

plt.plot(t, theta_list)
plt.axhline(theta_list[0] * math.exp(-math.pi))
plt.show()

cap.release()
cv2.destroyAllWindows() # destroy all opened windows