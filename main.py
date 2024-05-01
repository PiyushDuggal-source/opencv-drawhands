# import cv2
# import mediapipe as mp
#
# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# mp_hands = mp.solutions.hands
#
# camera = cv2.VideoCapture(0)
# hands = mp_hands.Hands()
#
# while True:
#     data, image = camera.read()
#
#     # flip the img
#     image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
#
#
#     output_hands = hands.process(image)
#
#     all_hands = output_hands.multi_hand_landmarks
#     print(all_hands)
#
#     if all_hands:
#         for hand in all_hands:
#             mp_drawing.draw_landmarks(image, hand)
#
#     cv2.imshow("Hands", image)
#     key = cv2.waitKey(100)
#     if key == 27:
#         break
#
# camera.release()
#
# cv2.destroyAllWindows()
import mediapipe as mp
import cv2
import numpy as np

mp_hands = mp.solutions.hands.Hands()
drawing_options = mp.solutions.drawing_utils

url = "http://192.168.1.8:8080/video"
camera = cv2.VideoCapture(0)

fx1, fx2, fy1, fy2 = 0, 0, 0, 0
sx1, sx2, sy1, sy2 = 0, 0, 0, 0

drawLine = False

listOfCord = []

d = {k: [] for k in range(21)}
count = 0

while True:
    data, image = camera.read()
    image_height, image_width, image_depth = image.shape
    image = cv2.flip(image, 1)
    rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output_hands = mp_hands.process(rgb_img)
    all_hands = output_hands.multi_hand_landmarks
    print(d)

    if all_hands:
        print(len(all_hands))

        if len(all_hands) == 2:
            firstHand = all_hands[0]
            secondHand = all_hands[1]

            firstForeFinger = firstHand.landmark[8]
            firstThumb = firstHand.landmark[4]
            secondForeFinger = secondHand.landmark[8]
            secondThumb = secondHand.landmark[4]

            fx1, fy1 = int(firstForeFinger.x * image_width), int(
                firstForeFinger.y * image_height
            )
            fx2, fy2 = int(firstThumb.x * image_width), int(firstThumb.y * image_height)

            print(fx1, fy1, fx2, fy2)

            cv2.circle(image, (fx1, fy1), 3, (0, 255, 255))
            cv2.circle(image, (fx2, fy2), 3, (0, 255, 255))

            sx1, sy1 = int(secondForeFinger.x * image_width), int(
                secondForeFinger.y * image_height
            )
            sx2, sy2 = int(secondThumb.x * image_width), int(
                secondThumb.y * image_height
            )

            cv2.circle(image, (sx1, sy1), 3, (0, 255, 255))
            cv2.circle(image, (sx2, sy2), 3, (0, 255, 255))

            print(fx1, fy1)

            d1 = int(np.sqrt((fx1 - sx1) ** 2 + (fy1 - sy1) ** 2))
            d2 = int(np.sqrt((fx2 - sx2) ** 2 + (fy2 - sy2) ** 2))
            d3 = int(np.sqrt((fx1 - fx2) ** 2 + (fy1 - fy2) ** 2))
            d4 = int(np.sqrt((sx1 - sx2) ** 2 + (sy2 - sy1) ** 2))

            d3_midX, d3_midY = ((fx1 + fx2) // 2), ((fy1 + fy2) // 2)
            d4_midX, d4_midY = ((sx1 + sx2) // 2), ((sy1 + sy2) // 2)

            if (d1 < 40 and d2 < 40) and (d3 < 40 and d4 < 40):
                drawLine = True

            if drawLine:
                cv2.line(image, (d3_midX, d3_midY), (d4_midX, d4_midY), (0, 255, 0), 3)
                # cv2.line(image, (fx2, fy2), (sx2, sy2), (0, 255, 0), 3)

            if d3 > 50 and d4 > 50:
                drawLine = False
                # d[1] = [(d3_midX, d3_midY), (d4_midX, d4_midY)]
                # listOfCord.append([(d3_midX, d3_midY), (d4_midX, d4_midY)])

            if d3 > 39 and d4 > 39 and drawLine:
                d[count] = [(d3_midX, d3_midY), (d4_midX, d4_midY)]

    for key, value in d.items():
        if key < count:
            continue

        if len(value) > 0:
            count += 1

    for key, value in d.items():
        if len(value) > 0:
            cv2.line(image, d[key][0], d[key][1], (255, 0, 255), 3)

    print("count", count, d[count])
    # if count == 0:
    #     if len(d[count]) > 0:
    #         cv2.line(image, d[count][0], d[count][1], (255, 0, 255), 3)
    # elif len(d[count - 1]) > 0:
    #     cv2.line(image, d[count- 1][0], d[count- 1][1], (255, 0, 255), 3)
    # cv2.line(image, listOfCord[0][0], listOfCord[0][1], (255, 0, 255), 5)

    # for id, lm in enumerate(firstHand.landmark):
    #     x = int(lm.x * image_width)
    #     y = int(lm.y * image_height)
    #
    #     if id == 8:
    #         fx1 = x
    #         fy1 = y
    #         cv2.circle(image, (x, y), 3, (0, 255, 255))
    #
    #     if id == 4:
    #         fx2 = x
    #         fy2 = y
    #         cv2.circle(image, (x, y), 3, (0, 255, 255))
    #
    # for id, lm in enumerate(firstHand.landmark):
    #     x = int(lm.x * image_width)
    #     y = int(lm.y * image_height)
    #
    #     if id == 8:
    #         fx1 = x
    #         fy1 = y
    #         cv2.circle(image, (x, y), 3, (0, 255, 255))
    #
    #     if id == 4:
    #         fx2 = x
    #         fy2 = y
    #         cv2.circle(image, (x, y), 3, (0, 255, 255))
    #
    # for hand in all_hands:
    #     # drawing_options.draw_landmarks(image, hand)
    #     one_hand_landmark = hand.landmark

    # for id, lm in enumerate(one_hand_landmark):
    #     x = int(lm.x * image_width)
    #     y = int(lm.y * image_height)
    #
    #     if id == 12:
    #         x1 = x
    #         y1 = y
    #         cv2.circle(image, (x, y), 3, (0, 255, 255))
    #
    #     if id == 0:
    #         x2 = x
    #         y2 = y
    #         cv2.circle(image, (x, y), 3, (0, 255, 255))

    cv2.imshow("hands", image)

    key = cv2.waitKey(100)

    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
