# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 19:21:09 2020

@author: whip
"""

import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


def plot_graph_100(info_log):
    
    graph_data = []
    for te in info_log[3:]:
        graph_data.append([te[1]["inochi"][0][0], te[1]["inochi"][1][0]])
    
    graph_data = np.array(graph_data)
    #print(graph_data)
    columns = ["mikata_inochi", "teki_inochi"]
    
    graph_data_df = pd.DataFrame(data=graph_data, columns=columns)
    for each_row in graph_data_df.index.tolist():
        graph_data_df.loc[each_row, :] = 100 * graph_data_df.loc[each_row, :] / graph_data_df.loc[each_row, :].sum()
    
    print(graph_data_df)
    graph_data_df.to_csv("graph_data_100.csv")
    
    #ここからグラフのプロット
    fig, ax = plt.subplots()
    data_points = np.arange(len(graph_data_df.index))
    ax.bar(data_points, graph_data_df.loc[:,"mikata_inochi"], color="#9AD051")
    ax.bar(data_points, graph_data_df.loc[:,"teki_inochi"], bottom=graph_data_df.loc[:,"mikata_inochi"], color="#FF9962")
    ax.bar(data_points,0.6,bottom=50-0.3, color="#FFFFFF")  #勝敗ラインプロット
    ax.bar(data_points,0.6,bottom=(100- 1000/35 -0.3), color="#990000") #逆転可能ライン(敵が勝つ)
    ax.bar(data_points,0.6,bottom=(1000/17 -0.3), color="#FF0000") #逆転確実ライン(敵が勝つ)
    ax.bar(data_points,0.6,bottom=(100- 1000/17 -0.3), color="#0000FF") #逆転確実ライン(味方が勝つ)
    ax.bar(data_points,0.6,bottom=(1000/35 -0.3), color="#000099") #逆転可能ライン(味方が勝つ)
    
    ax.set_title("inochi (percentage)")
    ax.set_xticks([] * len(graph_data_df.index))
    
    #画像として保存
    graph_name = "graph_100.png"
    plt.savefig(graph_name)
    
    return graph_name

def plot_graph(info_log):
    
    graph_data = []
    for te in info_log[3:]:
        graph_data.append([te[1]["inochi"][0][0], te[1]["inochi"][1][0]])
    
    graph_data = np.array(graph_data)
    #print(graph_data)
    columns = ["mikata_inochi", "teki_inochi"]
    
    graph_data_df = pd.DataFrame(data=graph_data, columns=columns)
    
    print(graph_data_df)
    graph_data_df.to_csv("graph_data_raw.csv")
    
    #ここからグラフのプロット
    fig, ax = plt.subplots()
    data_points = np.arange(len(graph_data_df.index))
    ax.bar(data_points, graph_data_df.loc[:,"mikata_inochi"], color="#9AD051")
    ax.bar(data_points, graph_data_df.loc[:,"teki_inochi"], bottom=graph_data_df.loc[:,"mikata_inochi"], color="#FF9962")
    
    ax.set_title("inochi")
    ax.set_xticks([] * len(graph_data_df.index))
    
    #画像として保存
    graph_name = "graph_raw.png"
    plt.savefig(graph_name)
    
    return graph_name