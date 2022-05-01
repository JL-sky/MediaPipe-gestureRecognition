# -*- codeing=utf-8 -*-
# @Author:姜磊
# 人间烟火气，最抚凡人心
import cv2 as cv
import autopy
import numpy as np
from fingersVector import fingersUp,vectorSize
import pyautogui
import cvzone

pyautogui.FAILSAFE =False
pyautogui.PAUSE = 0.5

# 获取屏幕尺寸
wScr,hScr=autopy.screen.size()# 1536.0 864.0
# 设置鼠标坐标平滑值
clocX,clocY=0,0
plocX,plocY=0,0
smooth=9
frameR=100
def aiMouse(frame,landmarks):
    wCap, hCap = 1180, 640
    global plocX,plocY
    # 画摄像头屏幕区域
    cv.rectangle(frame, (frameR, frameR-40), (wCap - frameR+40, hCap - int(frameR*0.8)), (255,235,26), thickness=2)
    cv.rectangle(frame, (frameR, frameR - 70), (frameR + 110, frameR-40), (255,235,26), -1)
    cv.putText(frame, "screen", (frameR + 5, frameR - 50), cv.FONT_ITALIC, 1, (255, 255, 255), thickness=2)
    fingersUP = fingersUp(landmarks)  # 判断手指向上
    finger8 = landmarks[8]  # 食指指尖
    # finger12 = landmarks[12]  # 中值指尖
    if fingersUP[1] == 1 and fingersUP[2] == 0:  # 食指向上
        mouseX = np.interp(finger8[0], (frameR, wCap - frameR+40), (0, wScr))  # 由视频尺度等比例转换屏幕尺度
        mouseY = np.interp(finger8[1], (frameR, hCap - int(frameR)), (0, hScr))
        # 平滑鼠标坐标值
        clocX = plocX + (mouseX - plocX) / smooth
        clocY = plocY + (mouseY - plocY) / smooth

        autopy.mouse.move(clocX, clocY)  # 移动鼠标

        cv.circle(frame, (finger8[0], finger8[1]), 15, (255, 0, 255), -1)  # 画出食指指尖
        plocX, plocY = clocX, clocY

    if fingersUP[1] == 1 and fingersUP[4] == 1:  # 点击
        cv.circle(frame, (finger8[0], finger8[1]), 15, (255, 0, 255), -1)
        cv.circle(frame, (finger8[0], finger8[1]), 15, (0, 0, 255), -1)
        autopy.mouse.click()  # 点击鼠标

# 在每帧图像上一次性画出所有按钮
def drawAll(img,buttonList):
    imgNew=np.zeros_like(img,np.int8)
    num=0
    for button in buttonList:
        # 获取按钮位置及其大小
        x, y = button.pos
        w, h = button.size
        # 绘制初始按钮242,220,84
        cvzone.cornerRect(img, (x,y,w,h),20,rt=0,colorC=(242,220,84))#绘制按钮边角
        cv.rectangle(imgNew, (x, y), (x + w, y + h), (172,0,114), -1)#80,102,120
    # 设置背景透明度
    out=img.copy()
    alpha=0.3
    mask=imgNew.astype(bool)
    out[mask]=cv.addWeighted(img,alpha,imgNew,1-alpha,0,dtype=cv.CV_32F)[mask]

    for button in buttonList:
        num=(num+1)%41
        # 获取按钮位置及其大小
        x, y = button.pos
        if num == 30:  # 绘制特殊按钮
            cv.putText(out, button.text, (x, y + 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        elif num == 38:
            cv.putText(out, button.text, (x + 3, y + 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        elif num == 40:
            cv.putText(out, button.text, (x + 3, y + 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        else:  # 绘制字母按钮
            cv.putText(out, button.text, (x + 15, y + 60), cv.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    return out

class Button():
    def __init__(self,pos,text,size=[75,75]):
        self.pos=pos
        self.text=text
        self.size=size

# 创建按钮列表
buttonList=[]
keys=[["1","2","3","4","5","6","7","8","9","0"],
      ["Q","W","E","R","T","Y","U","I","O","P"],
      ["A","S","D","F","G","H","J","K","L","del"],
      ["Z","X","C","V","B","N","M","<-",".","->"]]
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 120, 100 * i + 100], key))#创建按钮对象

def aiKeyboard(frame,landmarks):
    frame=drawAll(frame,buttonList)
    # fingers=fingersUp(landmarks)
    num=0
    for button  in buttonList:
        num=(num+1)%41
        x,y=button.pos
        w,h=button.size

        finger8=landmarks[8]
        finger12=landmarks[12]
        # 选择
        if x<finger8[0]<x+w and y<finger8[1]<y+h:#43,49,75
            cv.rectangle(frame, (x, y), (x + w, y + h), (0,127,255), -1)
            if num==30:
                cv.putText(frame, button.text, (x, y + 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 6)
            elif num == 38:
                cv.putText(frame, button.text, (x-5, y + 60), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
            elif num == 40:
                cv.putText(frame, button.text, (x-5, y + 60), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
            else:
                cv.putText(frame, button.text, (x + 10, y + 70), cv.FONT_HERSHEY_PLAIN, 6, (255, 255, 255), 6)
            # 点击
            length = vectorSize(finger8, finger12)  # 计算食指指尖与中指指尖长度
            # print(length)
            if length < 35:
            # if (fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1):

                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), -1)
                if num==30:#删除键
                    cv.putText(frame, button.text, (x-20, y + 50), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    pyautogui.press(["backspace"])
                elif num==38:#左移动
                    cv.putText(frame, button.text, (x, y + 50), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    pyautogui.press(["left"])
                elif num==40:#右移动
                    cv.putText(frame, button.text, (x, y + 50), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    pyautogui.press(["right"])
                else:
                    cv.putText(frame, button.text, (x + 10, y + 50), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    str = button.text
                    pyautogui.typewrite(str)

    return frame

