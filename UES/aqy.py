#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pyautogui
import psutil
import os
import logging
import time
pyautogui.PAUSE = 1.5
logging.basicConfig(level=logging.INFO)


def open_aqyclient():
    has_opened = 'QyClient.exe' in [p.name() for p in psutil.process_iter()]
    if not has_opened:
        os.system('"C:\Program Files (x86)\Common Files\IQIYI Video\LStyle\QyClient.exe" --runplugin=qiyitvPlugin')
        time.sleep(10)
        has_opened = 'QyClient.exe' in [p.name() for p in psutil.process_iter()]
        if has_opened:
            logging.info('AiQiYi Client Opened Successfully')
        else:
            raise Exception('Cannot open AiQiYi Client!')
    else:
        print('aqyclient has opened')


def open_gui():
    # open QYClient GUI
    if not pyautogui.locateOnScreen(r'D:\Script\juanzitest\check_gui_open.PNG'):
        client_x,client_y = pyautogui.locateCenterOnScreen(r'D:\Script\juanzitest\aqy_open_tag.PNG')
        pyautogui.click(client_x,client_y)
        if pyautogui.locateOnScreen(r'D:\Script\juanzitest\check_gui_open.PNG'):
            print('Open GUI successfully')
        else:
            raise Exception('Cannot find AiQiYi GUI')
    else:
        print('aqyclient GUI has opened')


def play_shows():
    if pyautogui.locateOnScreen(r'D:\Script\juanzitest\not_playing.PNG') and pyautogui.locateOnScreen(r'D:\Script\juanzitest\play_last.PNG'):
        play_x,play_y = pyautogui.locateCenterOnScreen(r'D:\Script\juanzitest\play_last.PNG')
        pyautogui.click(play_x,play_y)
        if pyautogui.locateOnScreen(r'D:\Script\juanzitest\check_if_play.PNG'):
            print('Play shows successfully')
        else:
            print('Cannot Play Shows')
    else:
        print('aqyclient has played')


while True:
    open_aqyclient()
    open_gui()
    play_shows()
    time.sleep(10)









