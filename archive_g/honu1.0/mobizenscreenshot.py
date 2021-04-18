# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 20:01:58 2020

@author: whip
"""

#pywinautoによる特定ウィンドウのスクリーンショット
from pywinauto import application
import datetime

def screenshot_mobizen():
    app = application.Application().connect(path=r"C:\Program Files (x86)\RSUPPORT\Mobizen/Mobizen.exe")
    
    img = app[u"Rsupport Mobizen Mirroring"].capture_as_image()
    img_cropped = img.crop((23,85,325,624)) #実際のスマホ画面領域
    
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H_%M_%S")
    
    img_name = 'image/mobizensnapshot' + timestamp + '.png'
    print("保存します ",img_name)
    img_cropped.save(img_name)
    return img_name
    
def screenshot_mikata_inochi():
    app = application.Application().connect(path=r"C:\Program Files (x86)\RSUPPORT\Mobizen/Mobizen.exe")
    
    img = app[u"Rsupport Mobizen Mirroring"].capture_as_image()
    img_cropped = img.crop((30,112,97,121)) #味方のイノチ表示領域
    img_name = 'mikata_inochi.png'
    img_cropped.save(img_name)
    return img_name    

def screenshot_teki_inochi():
    app = application.Application().connect(path=r"C:\Program Files (x86)\RSUPPORT\Mobizen/Mobizen.exe")
    
    img = app[u"Rsupport Mobizen Mirroring"].capture_as_image()
    img_cropped = img.crop((254,112,321,121)) #敵のイノチ表示領域
    img_name = 'teki_inochi.png'
    img_cropped.save(img_name)
    return img_name    

def screenshot_game_info():
    app = application.Application().connect(path=r"C:\Program Files (x86)\RSUPPORT\Mobizen/Mobizen.exe")
    
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H_%M_%S")
    img_name = 'image/mobizensnapshot' + timestamp + '.png'
    
    img = app[u"Rsupport Mobizen Mirroring"].capture_as_image()
    print("保存します ",img_name)
    img.save(img_name)
    
    img_cropped = img.crop((23,85,325,146)) #イノチからコンボまでの情報
    img_cropped_name = 'image/game_info' + timestamp + '.png'
    print("保存します ",img_cropped_name)
    img_cropped.save(img_cropped_name)
    return img_cropped_name        
    
