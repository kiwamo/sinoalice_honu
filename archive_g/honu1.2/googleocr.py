# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 19:10:41 2020

@author: whip
"""

import requests
import base64
import json
import sys

def googleOCR(img_name):
    GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='
    #API_KEY =  # 取得したAPIキーを入力してください。
    
    # APIを呼び、認識結果をjson型で返す
    def request_cloud_vison_api(image_base64):
        api_url = GOOGLE_CLOUD_VISION_API_URL + API_KEY
        req_body = json.dumps({
            'requests': [{
                'image': {
                    'content': image_base64.decode('utf-8') # jsonに変換するためにstring型に変換する
                },
                'features': [{
                    'type': 'TEXT_DETECTION', # ここを変更することで分析内容を変更できる
                    #'maxResults': 10,
                }]
            }]
        })
        res = requests.post(api_url, data=req_body)
        return res.json()
    
    # 画像読み込み
    def img_to_base64(filepath):
        with open(filepath, 'rb') as img:
            img_byte = img.read()
        return base64.b64encode(img_byte)
    
    # 文字認識させたい画像を./img.pngとする
    img_base64 = img_to_base64(img_name)
    result = request_cloud_vison_api(img_base64)

    #認識した文字の位置など、すべての情報を出力
    #print("{}".format(json.dumps(result, indent=4)))
    
    #文字情報だけ表示
    #print(result["responses"][0]["fullTextAnnotation"]["text"])
    #認識した単語と位置を出力
    try:
        result_text_and_position =[]
        parttext = ""
        pos_x = 0.
        pos_y = 0.
        n_x = 0
        n_y = 0
        
        for c in result["responses"][0]["fullTextAnnotation"]["pages"][0]["blocks"]:    #1文字ずつ文字と位置を取得
            #print("c = ",c, "\n")
            for b in c["paragraphs"][0]["words"]:
                for a in b["symbols"]:
                    #print("a = ",a,"\n")
                    #print("     ",a["boundingBox"]["vertices"], "  ", a["text"],"\n")
                    parttext += a["text"]
                    #print(a["boundingBox"]["vertices"])
                    for verti in a["boundingBox"]["vertices"]: #googleから返ってくる座標情報のところでx軸が抜けてるとかあるんだけど　なにこれええｗ
                        if "x" in verti:
                            pos_x += verti["x"]
                            n_x += 1
                        if "y" in verti:
                            pos_y += verti["y"]
                            n_y += 1
                        #n += 1
   
                    if "property" in a:
                        if "detectedBreak" in a["property"]:
                            #print("        ",a["property"],"\n")
                            if a["property"]["detectedBreak"]["type"] == "LINE_BREAK" or "EOL_SURE_SPACE" or "HYPHEN":
                                result_text_and_position.append([parttext, [pos_x / n_x, pos_y / n_y] ])
                                
                                parttext = ""
                                #n = 0
                                n_x = 0
                                n_y = 0
                                pos_x = 0.
                                pos_y = 0.
                            elif a["property"]["detectedBreak"]["type"] == "SPACE" or "SURE_SPACE":
                                parttext += " "
                            else:
                                print("知らないBreakがあります ",a["property"]["detectedBreak"]["type"])
                                pass
                            
        return result_text_and_position
    except KeyError:
        print("文字情報を取得出来ませんでした。")
        return []