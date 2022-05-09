# -*- codeing=utf-8 -*-
# @Author:千钧
# 人间烟火气，最抚凡人心
import math

# 计算向量2范数
def vectorSize(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

# 余弦定理计算向量夹角
def vectorAngle(p1,p2,p3):
    b = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    c = math.sqrt((p2[0] - p3[0]) ** 2 + (p2[1] - p3[1]) ** 2)
    a = math.sqrt((p3[0] - p1[0]) ** 2 + (p3[1] - p1[1]) ** 2)
    if ((2 * b * c)>1e-10):
        angle = math.acos(((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)))
    return math.degrees(angle)

# 由坐标点构造向量
def mkVector(p1,p2):
    return [(p1[0]-p2[0]),(p1[1]-p2[1])]

# 计算两个向量的夹角
def vectorAngle2(v1,v2):
    nor=0.0
    a=0.0
    b=0.0
    for x,y in zip(v1,v2):
        nor+=x*y#向量内积
        a+=x**2
        b+=y**2
    if a==0 or b==0:
        return None
    cosTheta=nor/math.sqrt(a*b)
    angle=math.acos(cosTheta)
    return math.degrees(angle)

# 判断手指是否张开
def fingersUp(landmarks):
    fingers=[]
    # 大拇指
    if vectorAngle(landmarks[0],landmarks[3],landmarks[4])>130:
        fingers.append(1)
    else:
        fingers.append(0)

    # 食指
    if vectorSize(landmarks[0],landmarks[8])>vectorSize(landmarks[0],landmarks[6]):
        fingers.append(1)
    else:
        fingers.append(0)

    # 中指
    if vectorSize(landmarks[0],landmarks[12])>vectorSize(landmarks[0],landmarks[10]):
        fingers.append(1)
    else:
        fingers.append(0)

     # 无名指
    if vectorSize(landmarks[0],landmarks[16])>vectorSize(landmarks[0],landmarks[14]):
        fingers.append(1)
    else:
        fingers.append(0)

     # 小拇指
    if vectorSize(landmarks[0],landmarks[20])>vectorSize(landmarks[0],landmarks[18]):
        fingers.append(1)
    else:
        fingers.append(0)

    return fingers
