#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pyautogui
import psutil
import os
import logging
import time
pyautogui.PAUSE = 1.5
def open_aqyclient():
    has_opened = 'QyClient.exe' in [p.name() for p in psutil.process_iter()]
    if not has_opened:
        os.system('"C:\Program Files (x86)\Common Files\IQIYI Video\LStyle\QyClient.exe" --runplugin=qiyitvPlugin')
        time.sleep(10)
        has_opened = 'QyClient.exe' in [p.name() for p in psutil.process_iter()]
        if has_opened:
            print('AiQiYi Client Opened Successfully')
        else:
            raise Exception('Cannot open AiQiYi Client!')
    else:
        print('aqyclient has opened')

def open_gui():
#open QYClient GUI
    if not pyautogui.locateOnScreen('check_gui_open.PNG'):
        client_x,client_y = pyautogui.locateCenterOnScreen('aqy_open_tag.PNG')
        pyautogui.click(client_x,client_y)
        if pyautogui.locateOnScreen('check_gui_open.PNG'):
            print('Open GUI sucessfully')
        else:
            raise Exception('Cannot find AiQiYi GUI')
    else:
        print('aqyclient GUI has opened')

def play_shows():
    if pyautogui.locateOnScreen('not_playing.PNG') and pyautogui.locateOnScreen('play_last.PNG'):
        play_x,play_y = pyautogui.locateCenterOnScreen('play_last.PNG')
        pyautogui.click(play_x,play_y)
        if pyautogui.locateOnScreen('check_if_play.PNG'):
            print('Play shows sucessfully')
        else:
            print('Cannot Play Shows')
    else:
        print('aqyclient has played')


while True:
    open_aqyclient()
    open_gui()
    play_shows()
    time.sleep(10)









