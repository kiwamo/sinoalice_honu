# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 20:05:28 2020

@author: whip
"""

import mobizenscreenshot as ms
import sinopcscreenshot as ss
import googleocr as go
import re
import Levenshtein

def get_game_info_dict(mode, last_inochi, last_time_delay):
    
    if mode == "mobile":
        img_name = ms.screenshot_game_info()
        img_size = [302, 61] #幅302(0-301), 高さ61(0-60)
        
    elif mode == "pc":
        img_name = ss.screenshot_sinopc_game_info()
        img_size = [486, 98] #幅486(0-485), 高さ98(0-97)
        
    result = go.googleOCR(img_name)

    #img_name = "image/game_info2020-02-15 20_29_53.png"
    #↓オソウジ中のresult
    #result = [['歩くような迷さで', [40.5, 16.625]], ['3.906 120', [39.5, 32.0]], ['バトルに戻る', [262.9375, 18.5]], ['9:15', [155.25, 39.25]], ['1.609.485', [265.1111111111111, 41.0]], ['1.067combo', [263.7, 53.0]], ['1.171combo', [28.15, 58.4]]]
    #↓三角が7になってしまう問題
    #result = [['7秘密結社荒神▽', [63.875, 17.375]], ['結婚おめでとう!', [424.1875, 17.9375]], ['114,570', [62.142857142857146, 50.5]], ['Majesty', [34.142857142857146, 70.5]], ['355combo', [61.0, 86.125]], ['19:09', [241.1, 49.9]], ['371.466', [421.35714285714283, 50.5]], ['537combo', [428.875, 85.875]]]
    results = [word for word in result if word[0] != ""] #単語要素が空のものを削除
    print("\nraw data = ", results)
    #print([str(a) for a in range(1,10)])
    
    mikata_inochi = ""
    teki_inochi = ""
    
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
            
            combolike = re.sub("[0-9]*","",res[0])
            if Levenshtein.distance(combolike, "combo") < 3: #combo　comboとの編集距離が3未満ならコンボ情報
                try:
                    res[0] = int(res[0].replace(combolike, ""))
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
                    
            elif res[1][1] < (img_size[1] / 61 * 40): #(mode=mobileのとき)それ以外の、コンボより上側(y座標が40未満)にある情報はイノチの数字
                if res[1][0] < (img_size[0] / 302 * 100): #(mode=mobileのとき)x座標が100未満なら味方のイノチ情報
                    try:
                        int(res[0])
                        mikata_inochi += res[0]
                    except ValueError:
                        print("予期しない値が代入されました。 イノチ ", res)
                        other.append(res)
                elif res[1][0] > (img_size[0] / 302 * 210): #(mode=mobileのとき)x座標が210以上なら敵のイノチ情報
                    try:
                        int(res[0])
                        teki_inochi += res[0]
                    except ValueError:
                        print("予期しない値が代入されました。 イノチ ", res)
                        other.append(res)
                else:
                    other.append(res)
            else:
                other.append(res)
        
        else:
            other.append(res)
    last_mikata_inochi = last_inochi[0][0]
    last_teki_inochi = last_inochi[1][0]
    try:
        mikata_inochi_list = [last_mikata_inochi, int(mikata_inochi)]
        teki_inochi_list = [last_teki_inochi, int(teki_inochi)]
        
        # どっちのイノチも前回のほうがでかかったら取得ミス
        if last_mikata_inochi > int(mikata_inochi) and last_teki_inochi > int(teki_inochi):
            print("イノチ情報の取得に失敗しました。inochi = ", inochi)
            error_flag[0] = 1
        
        # どっちかが前回の方がでかかったら、値を詳しく調査　ただし、前回まで取得ミスが重なっていたら、どうなってるかわからないので見逃す
        elif( last_mikata_inochi > int(mikata_inochi) or last_teki_inochi > int(teki_inochi) ) and last_time_delay[0] < 3:
            morau = max([mikata_inochi_list, teki_inochi_list], key=lambda x:x[1]-x[0])
            ageru = min([mikata_inochi_list, teki_inochi_list], key=lambda x:x[1]-x[0])
            print("\nイノチ移動率: ",1 - ageru[1] / ageru[0], 1 - ageru[1] / ageru[0])

            # もらう側が相手の0.15倍から0.3倍くらいもらってるかチェック 広めにとります
            # あげる側が自分の0.15倍から0.3倍くらいあげてるかチェック　広めに取ります
            if 0.0 < (morau[1] - morau[0]) / ageru[0] < 0.6 and 0.1 < 1 - ageru[1] / ageru[0] < 0.6:
                pass
            else:
                print("イノチ情報の取得に失敗しました。 morau = ", morau, "ageru = ", ageru, "イノチ移動率: ",(morau[1] - morau[0]) / ageru[0], 1 - ageru[1] / ageru[0])
                error_flag[0] = 1
            
    except:
        pass
        
    
    if mikata_inochi != "" and teki_inochi != "":
        try:
            inochi = [[int(mikata_inochi),[img_size[0]/302* 40.833, img_size[1]/61* 30.0]], [int(teki_inochi),[img_size[0]/302* 264.17, img_size[1]/61* 32.5]]] #座標はmode=mobileのときのそれっぽい適当な値
        except ValueError:
            print("予期しない値が代入されました。 味方イノチ ", mikata_inochi, "敵イノチ", teki_inochi)
    
    # ちゃんと想定通り値が入ってるかをある程度チェック、イノチとコンボを味方,相手の順になるよう並び替え
    if len(inochi) != 2:
        print("イノチ情報の取得に失敗しました。inochi = ", inochi)
        error_flag[0] = 1
    #else:
    #    if inochi[0][1][0] > inochi[1][1][0]: #イノチのx座標がインデックス0 > 1なら、逆に入っている 上でx座標で分岐を行っているのでこれは不要になったはず
    #        inochi[0], inochi[1] = inochi[1], inochi[0] #入れ替え
    
    if len(combo) != 2:
        print("コンボ情報の取得に失敗しました。combo = ", combo)
        error_flag[1] = 1
    else:
        if combo[0][1][0] > combo[1][1][0]: #コンボのx座標がインデックス0 > 1なら、逆に入っている
            combo[0], combo[1] = combo[1], combo[0] #入れ替え
            
    if len(time_sec) != 1 or time_sec[0][0] > 1200:
        print("残り時間情報の取得に失敗しました。time_sec = ", time_sec)
        error_flag[2] = 1
    
    result_dict = {"inochi" : inochi, "combo" : combo, "time_sec" : time_sec, "other" : other, "error_flag" : error_flag}
    
    print("\nmodified data = ", result_dict)
    return [img_name, result_dict]

# get_game_info_dict("pc")
