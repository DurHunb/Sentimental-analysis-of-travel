from pyltp import SentenceSplitter
import jieba.posseg as pseg
import jieba
import math,time

class SoPmi:
    def __init__(self):
        self.candipos_path = './data/candi_pos.txt'#种子正向
        self.candineg_path = './data/candi_neg.txt'#种子负向
        self.sentiment_path = './data/sentiment_words.txt'



    #计算次数
    def collect_cowords(self, sentiment_path, seg_data):
        def check_words(sent):
            if set(sentiment_words).intersection(set(sent)):
                return True
            else:
                return False
        cowords_list = list()
        window_size = 5
        count = 0
        sentiment_words = [line.strip().split('\t')[0] for line in open(sentiment_path)]
        for sent in seg_data:
            count += 1
            if check_words(sent):
                for index, word in enumerate(sent):
                    if index < window_size:
                        left = sent[:index]
                    else:
                        left = sent[index - window_size: index]
                    if index + window_size > len(sent):
                        right = sent[index + 1:]
                    else:
                        right = sent[index: index + window_size + 1]
                    context = left + right + [word]
                    if check_words(context):
                        for index_pre in range(0, len(context)):
                            if check_words([context[index_pre]]):
                                for index_post in range(index_pre + 1, len(context)):
                                    cowords_list.append(context[index_pre] + '@' + context[index_post])
        return cowords_list

    #计算So-Pmi值
    def collect_candiwords(self, seg_data, cowords_list, sentiment_path):

		def compute_mi(p11, p21, p1,p2):
            try: 
				number=((p11) / (p21)) * ((p2)/(p1))
				return number
			else:
				return 0
        #设置条件
        def collect_worddict(hitt_pos,hitt_neg,hitt_P,hitt_N):
            H=hitt_pos+hitt_neg
			if (hitt_pos/H)>0.89 and (hitt_neg/H)>0.89
				return compute_mi(0, 0, 0,0)
			elif (hitt_pos)<500000 and (hitt_neg)<500000
				return compute_mi(0, 0, 0,0)
			elif (hitt_pos/H-hitt_neg/H)<0.05
				return compute_mi(0, 0, 0,0)
			else:
				return compute_mi(hitt_pos,hitt_neg,hitt_P,hitt_N)

		def baidu_search(keyword,pn):
			  p= {'wd': keyword} 
			  res=urllib2.urlopen(("http://www.baidu.com/s?"+urllib.urlencode(p)+"&pn={0}&cl=3&rn=100").format(pn))
			  html=res.read()
			  return html
        #代入到网页计算
        def compute_sopmi(candi_words, pos_words, neg_words, word_dict, co_dict, all):
            #定义请求的头信息
			headers = {"User-Agent" : "Mozilla......"}

			#用户输入查询关键字
			keyword = raw_input("请输入要查询的关键字:")

			#变为字典处理
			wd = {'wd' : keyword}

			#对关键字进行url编码处理
			wd = urllib.urlencode(wd)

			#拼接url
			fullurl = url + wd

			#构建请求对象
			request = urllib2.Request(fullurl,headers = headers)

			#请求网页获取响应
			response = urllib2.urlopen(request)
			print(response.read())
            return pmi_dict

        word_dict, all = collect_worddict(seg_data)
        co_dict, candi_words = collect_cowordsdict(cowords_list)
        pos_words, neg_words = collect_sentiwords(sentiment_path, word_dict)
        pmi_dict = compute_sopmi(candi_words, pos_words, neg_words, word_dict, co_dict, all)
        return pmi_dict

    #保存
    def save_candiwords(self, pmi_dict, candipos_path, candineg_path):
        def get_tag(word):
            if word:
                return [item.flag for item in pseg.cut(word)][0]
            else:
                return 'x'
        pos_dict = dict()
        neg_dict = dict()
        f_neg = open(candineg_path, 'w+')
        f_pos = open(candipos_path, 'w+')

        for word, word_score in pmi_dict.items():
            if word_score > 0:
                pos_dict[word] = word_score
            else:
                neg_dict[word] = abs(word_score)

        for word, pmi in sorted(pos_dict.items(), key=lambda asd:asd[1], reverse=True):
            f_pos.write(word + ',' + str(pmi) + ',' + 'pos' + ',' + str(len(word)) + ',' + get_tag(word) + '\n')
        for word, pmi in sorted(neg_dict.items(), key=lambda asd:asd[1], reverse=True):
            f_neg.write(word + ',' + str(pmi) + ',' + 'neg' + ',' + str(len(word)) + ',' + get_tag(word) + '\n')
        f_neg.close()
        f_pos.close()
        return
 
    def sopmi(self):#好像有点问题，下次记得看
        print('step 1/4:...seg corpus ...')
        start_time  = time.time()
        seg_data = self.seg_corpus(self.train_path, self.sentiment_path)
        end_time1 = time.time()
        print('step 1/4 finished:...cost {0}...'.format((end_time1 - start_time)))
        print('step 2/4:...collect cowords ...')
        cowords_list = self.collect_cowords(self.sentiment_path, seg_data)
        end_time2 = time.time()
        print('step 2/4 finished:...cost {0}...'.format((end_time2 - end_time1)))
        print('step 3/4:...compute sopmi ...')
        pmi_dict = self.collect_candiwords(seg_data, cowords_list, self.sentiment_path)
        end_time3 = time.time()
        print('step 1/4 finished:...cost {0}...'.format((end_time3 - end_time2)))
        print('step 4/4:...save candiwords ...')
        self.save_candiwords(pmi_dict, self.candipos_path, self.candineg_path)
        end_time = time.time()
        print('finished! cost {0}'.format(end_time - start_time))

def test():#冲吧
    sopmier = SoPmi()
    sopmier.sopmi()

test()
