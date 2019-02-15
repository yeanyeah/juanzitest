#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pyautogui
import psutil
import os
import logging
import time
import imagehash
import random
from PIL import Image,ImageFile


class AQY(object):
    """AiQiYi object,defines method to hang with QyClient.exe"""
    def __init__(self, cmd_line=None, log_directory_path=r'D:\AQY\log'):
        pyautogui.PAUSE = 1.5
        self.logger = logging.getLogger(self.__class__.__name__)
        self.process_name = 'QyClient.exe'
        self.monitor_interval = 600
        if not cmd_line:
            self.cmd_line = \
                r'"C:\Program Files (x86)\Common Files\IQIYI Video\LStyle\QyClient.exe" --runplugin=qiyitvPlugin'
        # save log and Name logfile depended on datetime
        if not os.path.exists(log_directory_path):
            os.makedirs(log_directory_path)
        self.log_file_path = os.path.join(log_directory_path,'AQY_{}.log'.format(
            time.strftime('%y-%m-%d-%H-%M-%S',time.localtime())
        ))
        logging.basicConfig(filename=self.log_file_path,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(module)s :%(message)s',
                            datefmt='[%Y-%m-%d %H:%M:%S]',
                            level=logging.INFO)

    def _check_running(self):
        """
        Check if QyClient is already running
        :return: boolean,True means QyClient running
        Example:
        self.check_running()
        """
        self.logger.info('Check AiQiYi running status')
        is_running = self.process_name in [p.name() for p in psutil.process_iter()]
        return is_running

    def start_app(self):
        """
        Start AiQiYi APP if QyClient is not running
        :return: None
        Example:
        self.start_app()
        """
        self.logger.info('Start AiQiYi APP')
        while not self._check_running():
            os.system(self.cmd_line)
        time.sleep(5)

    def close_app(self):
        """
        Stop AiQiYi APP if QyClient is running
        :return: None
        Example:
        self.stop_app()
        """
        self.logger.info('Close AiQiYi APP')
        if self._check_running():
            os.system('taskkill /F /IM ' + self.process_name)
        else:
            self.logger.info('There is not any process about AiQiYi, do nothing')

    @staticmethod
    def _check_if_icon_exist(icon_path):
        """
        Check if the given icon can be seen on the screen
        :return: boolean,True means the icon can be seen
        Arguments:
        str,the path of the icon
        """
        try:
            pyautogui.center(pyautogui.locateOnScreen(icon_path))
            return True
        except TypeError:
            return False

    @staticmethod
    def _move_mouse_to_center_of_the_icon(icon_path):
        """
        Move mouse pointer to icon
        :return: None
        Arguments:
        str,the path of the icon
        """
        client_x,client_y = pyautogui.locateCenterOnScreen(icon_path)
        pyautogui.moveTo(client_x,client_y)

    def maximize_aiqiyi_gui(self):
        """
        Maximize AiQiYi APP if QyClient is running
        :return: None
        Example:
        self.stop_app()
        """
        self.start_app()
        if not AQY._check_if_icon_exist(os.path.abspath('aiqiyi_lunbotai_icon.png')):
            AQY._move_mouse_to_center_of_the_icon(os.path.abspath('aqy_open_tag.PNG'))
            pyautogui.click()
        # Click aiqiyi_lunbotai_icon for avoiding aiqiyi video ui being covered
        AQY._move_mouse_to_center_of_the_icon(os.path.abspath('aiqiyi_lunbotai_icon.png'))
        pyautogui.click()

        # Close channel selection for precisely judging if the video play smoothly.
        if AQY._check_if_icon_exist(os.path.abspath('close_channel_selection_button.png')):
            AQY._move_mouse_to_center_of_the_icon(os.path.abspath('close_channel_selection_button.png'))
            pyautogui.click()

            # Move the mouse to other place for avoiding cover the button
            pyautogui.moveRel(0, -50, duration=0.25)

    @staticmethod
    def _compare_image_with_hash(image_file1, image_file2, max_dif=0):
        """
        Check if two pictures look like each other by imagehash api
        Arguments:
            image_file1(str): image file1 address
            image_file2(str): image file2 address
            max_dif(int): max hash different, the lower, the preciser
        :return:boolean,True if two pictures look like each other
        Example:
            AiQiYi._compare_image_with_hash('new_video_screen_shot.png', 'old_video_screen_shot.png')
        """
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        with open(image_file1, 'rb') as fp:
            hash_1 = imagehash.average_hash(Image.open(fp))
        with open(image_file2, 'rb') as fp:
            hash_2 = imagehash.average_hash(Image.open(fp))

        # Return True if two pictures look like each other
        if abs(hash_1 - hash_2) <= max_dif:
            return True
        else:
            return False

    def _check_if_video_playing(self):
        """
        check if video play smoothly
        :return: boolean,True means video plays smoothly
        Example:
        is_video_playing = self._check_if_video_playing()
        """
        self.logger.info('Check if the video is playing')
        AQY._move_mouse_to_center_of_the_icon(os.path.abspath('aiqiyi_lunbotai_icon.png'))
        #Get aiqiyi screen shot and save it
        x, y = pyautogui.position()
        new_img = pyautogui.screenshot(region=(x + 100, y + 100, 400, 400))
        new_img.save('new_video_screen_shot.png')
        # Save old_video_screen_shot.png if it is not exists for avoiding function error
        if not os.path.exists('old_video_screen_shot.png'):
            time.sleep(3)
            os.rename('new_video_screen_shot.png','old_video_screen_shot.png')
            new_img = pyautogui.screenshot(region=(x + 100, y + 100, 400, 400))
            new_img.save('new_video_screen_shot.png')
        # Compare new video screen shot with old video screen shot
        compare_old_screen = AQY._compare_image_with_hash('new_video_screen_shot.png', 'old_video_screen_shot.png')

        # Check if video not playing
        compare_idle_screen = AQY._check_if_icon_exist(os.path.abspath('idle_video_screen_shot.png'))

        # Delete old_video_screen_shot.png and rename new_video_screen_shot.png
        os.remove('old_video_screen_shot.png')
        os.rename('new_video_screen_shot.png', 'old_video_screen_shot.png')

        if compare_old_screen or compare_idle_screen:
            self.logger.info('Video has stopped...')
            return False
        else:
            self.logger.info('Video is playing...')
            return True

    def _select_a_channel_randomly(self):
        """
         select a channel randomly in AiQiYi
         :return:None
         Example:
         self._select_a_channel_randomly()
        """
        self.logger.info('Select a channel randomly in AiQiYi')

        click_times = random.randint(1, 10)
        self.logger.warning('Click next channel button for {} times'.format(click_times))
        AQY._move_mouse_to_center_of_the_icon(os.path.abspath('next_channel_button.png'))
        for index in range(click_times):
            pyautogui.click()

        # Move the mouse to other place for avoiding cover the button
        pyautogui.moveRel(0, 50, duration=0.25)

    def run(self):
        """Run the AiQiYi video software automatically"""
        while True:
            self.maximize_aiqiyi_gui()
            if not self._check_if_video_playing():
                self._select_a_channel_randomly()

            self.logger.info('Stop monitor AiQiYi for {} seconds'.format(self.monitor_interval))
            time.sleep(self.monitor_interval)


if __name__ == '__main__':
    app = AQY()
    app.run()









