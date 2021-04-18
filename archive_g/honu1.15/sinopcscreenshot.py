# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 15:31:14 2020

@author: whip
"""

#pywinautoによる特定ウィンドウのスクリーンショット
import os
#from pywinauto import application
import datetime
from PIL import ImageGrab, Image

def screenshot_sinopc():
    
    now = datetime.datetime.now()    
    today = create_todays_folder(now)
    timestamp = now.strftime("%Y-%m-%d %H_%M_%S")
    img_name = 'image/'+today+'/sinopcsnapshot' + timestamp + '.png'
    
    img = ImageGrab.grab(bbox=[717,119,1203,983])
    print("保存します ",img_name)
    img.save(img_name)
    
    return img_name        

def screenshot_sinopc_game_info():
    
    now = datetime.datetime.now()    
    today = create_todays_folder(now)
    timestamp = now.strftime("%Y-%m-%d %H_%M_%S")
    img_name = 'image/'+today+'/sinopcsnapshot' + timestamp + '.png'
    
    img = ImageGrab.grab(bbox=[717,119,1203,983])
    print("保存します ",img_name)
    img.save(img_name)
    
    img_cropped = img.crop((0,0,486,98)) #デフォルト位置でのスクショ？
    img_cropped_name = 'image/'+today+'/sinopc_game_info' + timestamp + '.png'
    print("保存します ",img_cropped_name)
    img_cropped.save(img_cropped_name)
    
    return img_cropped_name        


def create_todays_folder(now):
    today = now.strftime("%Y%m%d")
    new_dir_path ="image/"+today
    os.makedirs(new_dir_path, exist_ok=True)
    return today