# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 13:32:25 2020

@author: whip

参考
https://qiita.com/1ntegrale9/items/9d570ef8175cf178468f
"""


import time
import discord
import sinomain as sinowhip
import plot_graph as pg

#TOKEN = 

client = discord.Client()


@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    #auto_get_pic = False # どうやんのこれ
    interval = 15
    itr = 4 #int(1200 / interval )+2 #15秒前から0秒前の間にスタートしましょう
    mode = "pc"
    
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '!neko':
        await message.channel.send('にゃーん')

    if message.content == '!start':
        await message.channel.send("自動情報取得開始　間隔 : "+str(interval)+" 秒, 取得回数 "+str(itr)+" 回" )
        
        start_time = time.time()
        #info_logの初期化　座標は適当に実際のログから取ってきた値
        info_log = [["", {'inochi': [[0, [41.55555555555556, 38.5]], [0, [264.77777777777777, 31.0]]], 'combo': [[0, [40.75, 53.0]], [0, [263.15, 58.5]]], 'time_sec': [[1200, [155.125, 31.5]]], 'other': [], 'error_flag': [0, 0, 0, 0], 'time_delay': [0, 0, 0, 0]}]]
        
        for i in range(itr):
            [img_name, d] = sinowhip.get_game_info_dict(mode)
            info_log = log_append(info_log, img_name, d)
            status_message = "#"+str(i)+"  "
            
            if d["error_flag"] == [0,0,0,0]:
                status_message += "正常に取得しました"
                await message.channel.send(status_message)
                
            elif d["error_flag"] == [1,1,0,0]:
                for other_info in d["other"]:
                    if other_info[0] == "バトルに戻る":
                        status_message += "オソウジ中です"
                        await message.channel.send(status_message)
                        break
                
            else:
                status_message += "情報取得中にエラーが発生しました・。；"
                await message.channel.send(status_message)
                
            await message.channel.send(file=discord.File(img_name))    
            await send_game_info(d, info_log, interval, message)
            await send_additional_game_info(d, info_log, message)
            
            end_time = time.time()
            time.sleep(max((interval - (end_time - start_time) ),0))
            start_time = time.time()
        await message.channel.send("自動情報取得終了")
        
        print("\ninfo_log = ",info_log)
        graph_name = pg.plot_graph(info_log)
        await message.channel.send(file=discord.File(graph_name)) #積み上げグラフ
        graph_name = pg.plot_graph_100(info_log)
        await message.channel.send(file=discord.File(graph_name)) #100%積み上げグラフ
                
    if message.content == '!pic':
        [img_name, d] = sinowhip.get_game_info_dict()
        if d["error_flag"] == [0,0,0,0]:
            await message.channel.send(file=discord.File(img_name))
            await message.channel.send("正常に取得しました")
            await message.channel.send(str(d))
        elif d["error_flag"] == [1,1,0,0] and "バトルに戻る" in d["other"]:
            await message.channel.send("オソウジ中です")
        else:
            await message.channel.send(file=discord.File(img_name))
            await message.channel.send("情報取得中にエラーが発生しました・。；")
            await message.channel.send(str(d))
            
    if message.content == '!stop':
       # auto_get_pic = False
       pass
    
    if message.content == '!restart':
       # auto_get_pic = True
       pass
            
    if message.content == '!owari':
        await message.channel.send("(¦3[▓▓]")
        await client.close()

async def send_game_info(d, info_log, interval, message):
    text = "表示情報\n"
    if info_log[-1][1]["error_flag"][2] != 0:
        time_estimate = max(info_log[-1][1]["time_sec"][0][0] - info_log[-1][1]["time_delay"][2] * interval, 0)
        text += ("　残り時間   **"+str(time_estimate // 60)+":"+str(time_estimate % 60).zfill(2)+"** ("+str(time_estimate)+"秒)   (推定)\n")
    else:
        text += ("　残り時間   **"+str(info_log[-1][1]["time_sec"][0][0] // 60)+":"+str(info_log[-1][1]["time_sec"][0][0] % 60).zfill(2)+"** ("+str(info_log[-1][1]["time_sec"][0][0])+"秒)\n")
        
    text += ("　味方イノチ   **"+str(info_log[-1][1]["inochi"][0][0])+"** - **"+str(info_log[-1][1]["inochi"][1][0])+"**   相手イノチ")
    if info_log[-1][1]["error_flag"][0] != 0:
        text += "   ( __**"+str(info_log[-1][1]["time_delay"][0] * interval)+"**__ 秒前の情報)"
    text += "\n"
    
    """
    #コンボの情報はいちいち表示しないことにしました
    text += ("　味方コンボ   **"+str(info_log[-1][1]["combo"][0][0])+"** - **"+str(info_log[-1][1]["combo"][1][0])+"**   相手コンボ")
    if info_log[-1][1]["error_flag"][1] != 0:
        text += "   ( __**"+str(info_log[-1][1]["time_delay"][1] * interval)+"**__ 秒前の情報)"
    text += "\n"
    """
    if info_log[-1][1]["error_flag"][3] == 0:
        text += "　他に取得した文字情報 : "
        for other_word in info_log[-1][1]["other"]:
            text += (other_word[0] + ", ")
    
    await message.channel.send(text)

async def send_additional_game_info(d, info_log, message):
    fulltext ="追加情報\n"
    text_list = []
    
    if d["error_flag"][0] == 0:
        text_list.append(reverse_info(d))
    
    if len(text_list):
        for text in text_list:
            fulltext += ("　"+text+"\n")
    else:
        fulltext += ("なし")
    await message.channel.send(fulltext)

def reverse_info(d):
    reverse_text = ""
    ressei_0, yuusei_0 = d["inochi"][0][0], d["inochi"][1][0]
    
    if ressei_0 > yuusei_0:
        ressei_0, yuusei_0 = yuusei_0, ressei_0
    
    if ressei_0*2.5 < yuusei_0:
        if ressei_0*2.45 > yuusei_0:
            reverse_text += "1シップ圏外ですが、最大乱数だとシップ後逆転もありえます"
            return reverse_text
        
        reverse_text += "1シップ圏外です"
    
    else:
        reverse_cases = 0
        minimum_percent = -1
        for i in range(30,14,-1):
            ressei_1 = ressei_0 + yuusei_0 * i/100
            yuusei_1 = yuusei_0 - yuusei_0 * i/100
            if ressei_1 > yuusei_1:
                reverse_cases += 1
                minimum_percent = i
        reverse_probability = reverse_cases / 16
        reverse_text += ("1シップ逆転の可能性 **"+str(reverse_probability * 100)+" %**　　最低必要なイノチ移動率 **"+str(minimum_percent)+" %**")
    
    return reverse_text

def log_append(info_log, img_name, d):
    d["time_delay"] = [0, 0, 0, 0]
    
    if d["error_flag"][0] == 1:
        d["inochi"] = info_log[-1][1]["inochi"]
        d["time_delay"][0] = info_log[-1][1]["time_delay"][0] + 1
    
    if d["error_flag"][1] == 1:
        d["combo"] = info_log[-1][1]["combo"]
        d["time_delay"][1] = info_log[-1][1]["time_delay"][1] + 1

    if d["error_flag"][2] == 1:
        d["time_sec"] = info_log[-1][1]["time_sec"]
        d["time_delay"][2] = info_log[-1][1]["time_delay"][2] + 1
        
    info_log.append([img_name, d])
    #print("info_log = ", info_log)
    return info_log
    

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
