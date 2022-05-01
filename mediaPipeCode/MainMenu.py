# -*- codeing=utf-8 -*-
# @Author:姜磊
# 人间烟火气，最抚凡人心
import os
import re
import sys

from PySide2.QtCore import QFile, Qt
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QApplication, QMessageBox, QHeaderView, QTableWidgetItem
from PySide2.QtUiTools import QUiLoader
from  PySide2 import QtWidgets

def function_prompts():
    print(
        """
    手势识别功能描述：

        手势                含义                识别结果
        -------------------------------------------------
        ok                 播放                    1
        比心              继续播放                   6 
        中指                暂停                    4
        左挥手             上一曲                    8
        右挥手             下一曲                    7
        点赞              增加音量                   2
        拳头              降低音量                   3
        蜘蛛侠              关闭                     5
        """
    )

class Stats:

    def __init__(self):

        self.ui = QUiLoader().load('menu.ui')
        # 功能菜单
        self.menuFunc()
        # 音乐菜单
        self.menuMusic()

        self.ui.musicBrowser.append("music")

    def menuFunc(self):
        hand = [' ok ', '比心', ' 中指', ' 左挥手', ' 右挥手', ' 点赞', ' 拳头', ' 蜘蛛侠']
        func = ['播放', '继续播放', '暂停', '上一曲', '下一曲', '增加音量', '降低音量', '关闭']
        model = self.ui.funcTable
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
            music=re.sub('.mp3', '', names[name])
            musics.append(music)

        # self.ui.musicList.addItems(musics)

        model = self.ui.musicTable
        # 设置行列
        model.setColumnCount(1)
        model.setRowCount(len(names))
        # 设置表头
        model.setHorizontalHeaderLabels(['歌单'])
        # 添加数据
        for i in range(len(musics)):
            model.setItem(i, 0, QTableWidgetItem(musics[i]))

        # # 居中
        # for i in range(model.rowCount()):
        #     for j in range(model.columnCount()):
        #         if model.item(i, j):
        #             model.item(i, j).setTextAlignment(Qt.AlignCenter)

        # 布局
        model.horizontalHeader().setStretchLastSection(True)
        # 垂直充满表格，拉伸的最后一行
        model.verticalHeader().setStretchLastSection(True)
        # 全部列拉伸
        model.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 全部行拉伸
        model.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)


def menu():
    app = QApplication([])
    # app = QApplication.instance([])
    # if app is None:
    #     app = QApplication(sys.argv)
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()


    app.setStyle('Fusion')
    stats = Stats()
    stats.ui.show()
    app.exec_()
# menu()