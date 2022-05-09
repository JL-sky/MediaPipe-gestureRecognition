# -*- codeing=utf-8 -*-
# @Author:千钧
# 人间烟火气，最抚凡人心
import mediapipe as mp
import cv2 as cv

# 绘制关键点与连接线函数
mp_drawing = mp.solutions.drawing_utils
handMsStyle=mp_drawing.DrawingSpec(color=(0,0,255),thickness=int(5))#关键点样式
handConStyle=mp_drawing.DrawingSpec(color=(0,255,0),thickness=int(8))#关键点连接线样式
#手部检测函数
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
        static_image_mode=False,#检测的是视频流还是静态图片，False为视频流，True为图片
        max_num_hands=1,#检测出手的最大数量
        min_detection_confidence=0.75,#首部检测的最小置信度，大于该值则认为检测成功
        min_tracking_confidence=0.75)#目标跟踪模型的最小置信度


def handLandmarks(frame):
    imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    result = hands.process(imgRGB)
    hand_point = result.multi_hand_landmarks  # 返回21个手部关键点的坐标，其值为比例
    result = hands.process(imgRGB)
    hand_point = result.multi_hand_landmarks  # 返回21个手部关键点的坐标，其值为比例

    landmarks = []
    # 当关键点存在时
    if hand_point:
        for handlms in hand_point:
            # print(handlms)
            # 绘制关键点及其连接线，参数：
            # 绘制的图片，关键点坐标，连接线，点样式，线样式
            mp_drawing.draw_landmarks(frame, handlms, mp_hands.HAND_CONNECTIONS, handMsStyle, handConStyle)
            for i, lm in enumerate(handlms.landmark):
                posX = int(lm.x * frame.shape[1])  # lm.x表示在图片大小下的比例，乘以图片大小将其转换为队形坐标
                posY = int(lm.y * frame.shape[0])
                landmarks.append((posX, posY))  # 21个手部关键点坐标
                # 显示关键点
                cv.putText(frame, str(i), (posX, posY), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), thickness=2)

        return landmarks
    else:
        return "error"
