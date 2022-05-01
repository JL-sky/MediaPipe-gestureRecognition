# -*- codeing=utf-8 -*-
# @Author:姜磊
# 人间烟火气，最抚凡人心

import os
import re

import pygame

abs_path=os.path.abspath("..")
path=abs_path+r"\music"+r"\\"[-1]
# 遍历文件夹
names = os.listdir(path)


# 初始化音乐播放器
pygame.mixer.init()
# 打开音乐播放器
music = pygame.mixer.music
# music=pygame.mixer.Sound
# 初始化播放队列序号
num = 0
# 初始化音乐音量
volume = 0.2



def musicPlay(command):
    global num, volume
    if command in [1, 2, 3, 4, 5, 6, 7, 8]:
        # print(command)
        # 播放
        if command == 1:
            music.load(path + names[num])
            music.play()
        # 暂停
        if command == 4:
            music.pause()
        # 继续播放
        if command == 6:
            music.unpause()
        # 上一曲
        if command == 8:
            num = num - 1
            music.load(path + names[num])

            # music.load("./music/" + names[num])
            music.play()
        # 下一曲
        if command == 7:
            num = (num + 1) % len(names)
            music.load(path + names[num])

            # music.load("./music/" + names[num])
            music.play()

        # 增加音量
        if command == 2:
            if volume < 10:
                volume = volume + 1
                music.set_volume(volume)
        # 降低音量
        if command == 3:
            if volume > 0:
                volume = volume - 1
                music.set_volume(volume)
        # 关闭
        if command == 5:
            os.kill(os.getpid(), 9)

        # print("正在播放第" + str(num + 1) + "音乐：" + names[num])
        print("当前播放音量：", volume)
        musicName = re.sub('.mp3', '', names[num])
        # print(musicName,volume)
        return musicName
