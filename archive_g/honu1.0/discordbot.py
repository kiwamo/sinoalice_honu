# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 13:32:25 2020

@author: whip

参考
https://qiita.com/1ntegrale9/items/9d570ef8175cf178468f
"""

import discord
import sinomain as sinowhip
import time

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
    itr = int(1200 / interval )+1
    
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '!neko':
        await message.channel.send('にゃーん')

    if message.content == '!start':
        await message.channel.send("自動情報取得開始　間隔 : "+str(interval)+" 秒, 取得回数 "+str(itr)+" 回" )
        
        start_time = time.time()
        for i in range(itr):
            
            [img_name, d] = sinowhip.get_game_info_dict()
            if d["error_flag"] == [0,0,0,0]:
                await message.channel.send("正常に取得しました")
                
            elif d["error_flag"] == [1,1,0,0]:
                for other_info in d["other"]:
                    if other_info[0] == "バトルに戻る":
                        await message.channel.send("オソウジ中です")
                        break
                
            else:
                await message.channel.send("情報取得中にエラーが発生しました・。；")
                
            await message.channel.send(file=discord.File(img_name))    
            await send_game_info(d, message)
            end_time = time.time()
            time.sleep(interval - (end_time - start_time) )
            start_time = time.time()
        await message.channel.send("自動情報取得終了")
                
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

async def send_game_info(d, message):
    text = "・。・\n"
    if len(d["time_sec"]) == 1:
        text += ("　残り時間   **"+str(d["time_sec"][0][0] // 60)+":"+str(d["time_sec"][0][0] % 60)+"** ("+str(d["time_sec"][0][0])+"秒)\n")
    if len(d["inochi"]) == 2:
        text += ("　味方イノチ   **"+str(d["inochi"][0][0])+"** - **"+str(d["inochi"][1][0])+"**   相手イノチ\n")
    if len(d["combo"]) == 2:
        text += ("　味方コンボ   **"+str(d["combo"][0][0])+"** - **"+str(d["combo"][1][0])+"**   相手コンボ\n")
    if len(d["other"]):
        text += "　他に取得した文字情報 : "
        for other_word in d["other"]:
            text += (other_word[0] + ", ")
    
    await message.channel.send(text)
    

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
