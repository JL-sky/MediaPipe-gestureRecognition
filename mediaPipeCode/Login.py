import os
import re
import time
import cv2 as cv
from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QHeaderView
from PySide2.QtUiTools import QUiLoader
from HandLandmarks import handLandmarks
from GestureRecognition import gestureRecognition,staticGestureRec
from MusicPlay import musicPlay
from GestureRecognition import gestureRecognition,staticGestureRec
from autoAI import aiMouse,aiKeyboard
import threading


# QtWidgets.QMainWindow,Qt.Ui_MainWindow
class Stats():

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit

        #加载登录UI界面
        self.ui = QUiLoader().load('login.ui')
        # 点击确定触发登录验证
        self.ui.login_btn.clicked.connect(self.login)
        # 点击取消关闭窗口
        self.ui.cancel_btn.clicked.connect(self.closeWin)
        # 虚拟鼠标与键盘同步并发启动
        self.cameraStart()

        # 加载菜单UI界面
        self.menu = QUiLoader().load('menu.ui')
    def login(self):
        # 获取键盘输入的账号密码
        username = self.ui.account_lineEdit.text()
        password = self.ui.password_lineEdit.text()
        # 账号密码输入正确
        if username == 'ADMIN' and password == '123':
            self.ui.close()#关闭登录界面
            self.menu.show()#显示菜单界面
            self.menuFunc()#手势功能菜单加载
            self.menuMusic()#音乐歌单加载
            self.playVideoFile()#加载手势识别视频流
            # return True
        else:
            QMessageBox.critical(
                self.ui,
                '登录',
                '登录失败，请重新输入！')

    def closeWin(self):
        self.ui.close()
        # exit(0)

    def menuFunc(self):
        hand = [' ok ', '比心', ' 中指', ' 左挥手', ' 右挥手', ' 点赞', ' 拳头', ' 蜘蛛侠']
        func = ['播放', '继续播放', '暂停', '上一曲', '下一曲', '增加音量', '降低音量', '关闭']
        model = self.menu.funcTable
        # 设置行列
        model.setColumnCount(2)
        model.setRowCount(8)
        # 设置表头
        model.setHorizontalHeaderLabels(['手势', '功能'])
        # 添加数据
        for i in range(len(hand)):
            model.setItem(i, 0, QTableWidgetItem(hand[i]))
        for i in range(len(func)):
            model.setItem(i, 1, QTableWidgetItem(func[i]))

        # 居中
        for i in range(model.rowCount()):
            for j in range(model.columnCount()):
                if model.item(i, j):
                    model.item(i, j).setTextAlignment(Qt.AlignCenter)

        # 布局
        model.horizontalHeader().setStretchLastSection(True)
        # 垂直充满表格，拉伸的最后一行
        model.verticalHeader().setStretchLastSection(True)
        # 全部列拉伸
        model.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 全部行拉伸
        model.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def menuMusic(self):
        abs_path = os.path.abspath("..")
        path = abs_path + r"\music" + r"\\"[-1]
        # 遍历文件夹
        names = os.listdir(path)
        musics=[]
        for name in range(len(names)):
            music=re.sub('.mp3', '', names[name])#正则去除.MP3后缀
            musics.append(music)

        model = self.menu.musicTable

        # 设置行列
        model.setColumnCount(1)
        model.setRowCount(len(names))
        # 设置表头
        model.setHorizontalHeaderLabels(['歌单'])
        # 添加数据
        for i in range(len(musics)):
            model.setItem(i, 0, QTableWidgetItem(musics[i]))

        # 布局
        model.horizontalHeader().setStretchLastSection(True)
        # 垂直充满表格，拉伸的最后一行
        model.verticalHeader().setStretchLastSection(True)
        # 全部列拉伸
        model.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 全部行拉伸
        model.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def playVideoFile(self):  # 播放影片

        # fps统计
        cTime = 0
        pTime = 0

        # 摄像头参数设置
        wCap, hCap = 640, 480
        # wCap, hCap = 1280, 720
        video = cv.VideoCapture(0, cv.CAP_DSHOW)
        video.set(3, wCap)
        video.set(4, hCap)

        # 帧差重心
        preCenter = [wCap / 2, hCap / 2]
        curCenter = [0, 0]
        preCommand = 0

        while True:

            ret, frame = video.read()
            frame = cv.flip(frame, 1)
            if ret:
                # 手部关键点检测
                landmarks = handLandmarks(frame)
                if not isinstance(landmarks, str):
                    # 手势命令识别
                    curCenter, command = gestureRecognition(frame, landmarks, preCenter)
                    preCenter = curCenter

                    # 控制音乐播放器
                    if (command != preCommand or command in [2, 3, 7, 8]):
                        musicName= musicPlay(command)
                        if musicName is not None:
                            self.menu.musicBrowser.setText(musicName)
                        preCommand = command
                # 帧率统计
                cTime = time.time()  # 现在的时间
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv.putText(frame, str(int(fps)), (20, 50), cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), thickness=2)

                # 在qt界面显示视频流
                QtImgBuf = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
                QtImg = QtGui.QImage(QtImgBuf.data, QtImgBuf.shape[1], QtImgBuf.shape[0], QtGui.QImage.Format_RGB32)
                self.menu.ImgDisp.setPixmap(QtGui.QPixmap.fromImage(QtImg))  # 在ImgDisp显示图像
                size = QtImg.size()
                self.menu.ImgDisp.resize(size)  # 根据帧大小调整标签大小
                self.menu.ImgDisp.show()  # 刷新界面
                cv.waitKey(1)

        # 完成所有操作后，释放捕获器
        video.release()

    def gestureCamera(self):

        # fps统计
        cTime = 0
        pTime = 0

        # 摄像头参数设置
        # wCap,hCap=640,480
        # wCap,hCap=1280,720
        wCap, hCap = 1100, 320
        video = cv.VideoCapture(0)
        video.set(3, wCap)
        video.set(4, hCap)

        while True:
            ret, frame = video.read()
            frame = cv.flip(frame, 1)
            if ret:
                # 手部关键点检测
                landmarks = handLandmarks(frame)
                if not isinstance(landmarks, str):

                    # 手势命令识别
                    command = staticGestureRec(landmarks)
                    if command == 5:
                        break

                    # 虚拟鼠标
                    aiMouse(frame, landmarks=landmarks)

                    # 虚拟键盘
                    frame = aiKeyboard(frame, landmarks=landmarks)

            # 帧率统计
            cTime = time.time()  # 现在的时间
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv.putText(frame, str(int(fps)), (20, 50), cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), thickness=2)

            # # 在qt界面显示视频流
            QtImgBuf = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
            QtImg = QtGui.QImage(QtImgBuf.data, QtImgBuf.shape[1], QtImgBuf.shape[0], QtGui.QImage.Format_RGB32)
            self.ui.framelabel.setPixmap(QtGui.QPixmap.fromImage(QtImg))  # 在ImgDisp显示图像
            size = QtImg.size()
            self.ui.framelabel.resize(size)  # 根据帧大小调整标签大小
            self.ui.framelabel.show()  # 刷新界面
            cv.waitKey(1)

    def cameraStart(self):#多线程启动
        tid=threading.Thread(target=self.gestureCamera)
        tid.start()




def logIn():
    app = QApplication([])
    app.setStyle('Fusion')
    stats = Stats()
    stats.ui.show()
    app.exec_()
    # return stats.login()
logIn()

# print(logIn())