# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 20:05:28 2020

@author: whip
"""

import mobizenscreenshot as ms
import googleocr as go
import re

def get_game_info_dict():

    img_name = ms.screenshot_game_info()
    
    result = go.googleOCR(img_name)

    #img_name = "image/game_info2020-02-15 20_29_53.png"
    #result = [['歩くような迷さで', [40.5, 16.625]], ['3.906 120', [39.5, 32.0]], ['バトルに戻る', [262.9375, 18.5]], ['9:15', [155.25, 39.25]], ['1.609.485', [265.1111111111111, 41.0]], ['1.067combo', [263.7, 53.0]], ['1.171combo', [28.15, 58.4]]]
    results = [word for word in result if word[0] != ""] #単語要素が空のものを削除
    print("raw data = ", results)
    #print([str(a) for a in range(1,10)])    
    
    inochi = [] #list[int]
    combo = [] #list[int]
    time_sec = [] # list[int]
    other = [] #list[str]
    error_flag = [0,0,0,0]
    
    for res in results:
        res[0] = res[0].replace(",", "")
        res[0] = res[0].replace(".", "")
        res[0] = res[0].replace(" ", "")
        
        if res[0][0] in [str(a) for a in range(0,10)]: #1文字目が0～9なら数字情報
            #print(res)
            
            if re.search("combo",res[0]):
                try:
                    res[0] = int(res[0].replace("combo",""))
                    combo.append(res)
                except ValueError:
                    print("予期しない値が代入されました。 コンボ ", res[0])
                    
            elif re.search(":",res[0]) and len(time_sec) < 1:
                try:
                    min_sec = res[0].split(":")
                    res[0] = int(min_sec[0]) * 60 + int(min_sec[1])
                    time_sec.append(res)
                except ValueError:
                    print("予期しない値が代入されました。 残り時間 ", res)     
                    
            elif len(inochi) < 2:
                try:
                    res[0] = int(res[0])
                    inochi.append(res)
                except ValueError:
                    print("予期しない値が代入されました。 イノチ ", res)    
                    
            else:
                other.append(res)
    
        else:
            other.append(res)
    
    # ちゃんと想定通り値が入ってるかをある程度チェック、イノチとコンボを味方,相手の順になるよう並び替え
    if len(inochi) != 2:
        print("イノチ情報の取得に失敗しました。inochi = ", inochi)
        error_flag[0] = 1
    else:
        if inochi[0][1][0] > inochi[1][1][0]: #イノチのx座標がインデックス0 > 1なら、逆に入っている
            inochi[0], inochi[1] = inochi[1], inochi[0] #入れ替え
            
    if len(combo) != 2:
        print("コンボ情報の取得に失敗しました。combo = ", combo)
        error_flag[1] = 1
    else:
        if combo[0][1][0] > combo[1][1][0]: #コンボのx座標がインデックス0 > 1なら、逆に入っている
            combo[0], combo[1] = combo[1], combo[0] #入れ替え
            
    if len(time_sec) != 1 or time_sec[0][0] > 1200:
        print("残り時間情報の取得に失敗しました。time_sec = ", time_sec)
        error_flag[2] = 1
    
    #イノチとコンボが味方,相手の順になるように並び替え

    
    result_dict = {"inochi" : inochi, "combo" : combo, "time_sec" : time_sec, "other" : other, "error_flag" : error_flag}
    
    print("modified data = ", result_dict)
    return [img_name, result_dict]