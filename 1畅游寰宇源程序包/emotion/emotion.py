# -*- coding = utf8 -*-
import jieba
import numpy as np
import os
import xlrd,xlwt
from tqdm import tqdm
from xlutils.copy import copy
#打开词典文件，返回列表
def open_dict(Dict = 'hahah', path='E:\MyPythonProject\工程文件\景点微博\emotion\\'):
    path = path + '%s.txt' % Dict
    dictionary = open(path, 'r', encoding='utf-8')
    dict = []
    for word in dictionary:
        word = word.strip('\n')
        try:
            word = word.strip()
        except:
            pass
        dict.append(word)
    return dict

def judgeodd(num):
    if (num % 2) == 0:
        return 'even'
    else:
        return 'odd'


#注意，这里你要修改path路径。
deny_word = open_dict(Dict = '否定词', path= r'emotion/')                   #打开否定词文档
posdict = open_dict(Dict = 'hao', path= r'emotion/')                         #打开积极情感词库
negdict = open_dict(Dict = 'huai', path= r'emotion/')                         #打开消极情感词库
word_2 = open_dict(Dict='2',path=r'emotion/')                               #打开副词库
word_1_5 = open_dict(Dict='1.5',path=r'emotion/')
word_1_25 = open_dict(Dict='1.25',path=r'emotion/')
word_1_2 = open_dict(Dict='1.2',path=r'emotion/')
word_0_8 = open_dict(Dict='0.8',path=r'emotion/')
word_0_5 = open_dict(Dict='0.5',path=r'emotion/')



def sentiment_score_list(dataset):    #主处理函数
    try:
        dataset = dataset.replace("，","。")
        seg_sentence = dataset.split('。')
    except:
        seg_sentence = []



    count2 = []
    p_grades = 0
    n_grades = 0
    for sen in seg_sentence: #循环遍历每一个评论
        segtmp = jieba.lcut(sen, cut_all=True)  #把句子进行分词，以列表的形式返回

        i = 0 #记录扫描到的词的位置
        a = 0 #记录情感词的位置
        poscount = 0 #积极词的第一次分值
        poscount2 = 0 #积极词反转后的分值
        poscount3 = 0 #积极词的最后分值（包括叹号的分值）
        negcount = 0
        negcount2 = 0
        negcount3 = 0
        for word in segtmp:
            poscount3 = 0
            negcount3 = 0
            if word == "":
                i += 1
                continue
            if word in posdict:  # 判断词语是否是情感词
                poscount += 1
                c = 0
                for w in segtmp[a:i]:  # 扫描情感词前的程度词
                    if w in word_2:
                        poscount *= 2.0
                    elif w in word_1_5:
                        poscount *= 1.5
                    elif w in word_1_25:
                        poscount *= 1.25
                    elif w in word_1_2:
                        poscount *= 1.2
                    elif w in word_0_8:
                        poscount *= 0.8
                    elif w in word_0_5:
                        poscount *= 0.5
                    elif w in deny_word:
                        c += 1
                if judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                    poscount *= -1.0
                    poscount2 += poscount
                    poscount = 0
                    poscount3 = poscount + poscount2 + poscount3
                    poscount2 = 0
                else:
                    poscount3 = poscount + poscount2 + poscount3
                    poscount = 0
                a = i + 1  # 情感词的位置变化

            elif word in negdict:  # 消极情感的分析，与上面一致
                negcount += 1
                d = 0
                for w in segtmp[a:i]:
                    if w in word_2:
                        poscount *= 2.0
                    elif w in word_1_5:
                        poscount *= 1.5
                    elif w in word_1_25:
                        poscount *= 1.25
                    elif w in word_1_2:
                        poscount *= 1.2
                    elif w in word_0_8:
                        poscount *= 0.8
                    elif w in word_0_5:
                        poscount *= 0.5
                    elif w in deny_word:
                        d += 1
                if judgeodd(d) == 'odd':
                    negcount *= -1.0
                    negcount2 += negcount
                    negcount = 0
                    negcount3 = negcount + negcount2 + negcount3
                    negcount2 = 0
                else:
                    negcount3 = negcount + negcount2 + negcount3
                    negcount = 0
                a = i + 1
            elif word == '！' or word == '!':  ##判断句子是否有感叹号
                for w2 in segtmp[::-1]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                    if w2 in posdict or negdict:
                        poscount3 += 2
                        negcount3 += 2
                        break
            i += 1 # 扫描词位置前移



            p_grades += poscount3
            n_grades -= negcount3

            # count1.append([poscount3, negcount3])
            count1 = []
    count2.append(p_grades)
    count2.append(n_grades)


    return count2

def sentiment_score(senti_score_list):
    score = []
    sum = 0
    for review in senti_score_list:
        sum=sum+review
        score.append(review)
    return sum

# data1 = '我悔恨万分'
# print(sentiment_score(sentiment_score_list(data1)))


