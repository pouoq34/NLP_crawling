from konlpy.tag import Okt
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

tokenizer = Okt()


news = pd.read_csv('/rawdata_7월.csv')
del news['Unnamed: 0']
keyword = news['content']

#for example!
word = []
word = keyword[:10].tolist() #리스트 형태로 변환
#word = keyword[:10] 처음에 이렇게 했다가 word가 시리즈 형태라 불가능햇승

def text_preprocessing(text, tokenizer):
    stopwords = ['을', '를', '이', '가', '은', '는', 'null', '들', '에', ] #불용어 설정
    tokenizer = Okt() #형태소 분석기
    token_list = []
    i = 0
    j=0

    for i in range(0,len(word)):
        txt = re.sub('의학|신문|기자|일간|일간|보사|뉴스', ' ', word[i])  # '의학 or ...'을 ' '으로 변경함
        token = tokenizer.nouns(txt)  # 형태소 분석
        #token = [t for t in token if t not in stopwords or type(t) != float]  # 형태소 분석 결과 중 stopwords에 해당하지 않는 것만 추출+
        token2 = " ".join(token)
        token_list.insert(j,token2) #insert랑 append의 차이점!!
        j+=1

    return token_list

# 형태소 분석기를 따로 저장한 이유는 후에 test 데이터 전처리를 진행할 때 이용해야 되기 때문
key = text_preprocessing(word,tokenizer)

key_df = pd.DataFrame({"keyword":key})
key_df.to_csv('/keywords.csv',encoding='utf-8-sig')


#명사 형태의 데이터 프레임 불러오기
news2 = pd.read_csv('/keywords.csv', encoding='utf-8-sig')

np.array(news2['keyword'].tolist())
news2_corpus = list(np.array(news2['keyword'].tolist()))

vect = CountVectorizer()
# 문서-단어 행렬
document_term_matrix = vect.fit_transform(news2_corpus)


# TF (Term Frequency)
news2_tf = pd.DataFrame(document_term_matrix.toarray(), columns=vect.get_feature_names())

news2_tf.loc['SUM1'] = news2_tf.sum(axis=0)
news_tf = news2_tf.loc['SUM1']

news_tf = pd.DataFrame(news_tf)
news_tf = news_tf.reset_index()
news_tf = news_tf.sort_values('SUM1', ascending=False)
#news_tf = news_tf.loc[news_tf['SUM1']>=5]

news_tf.to_csv('/news_tf.csv', encoding="utf-8-sig")


# DF (Document Frequency)
news_doc = len(news2_tf)
news_df = news2_tf.astype(bool).sum(axis=0) #시리즈 type
news_df = pd.DataFrame({'word':news_df.index, 'count1':news_df.values})
#news_df.to_csv('C/news_df.csv', encoding="utf-8-sig")

# IDF (Inverse Document Frequency)
#문서 수
D = 3961

news_df=news_df.set_index('word')

idf = np.log(D / (news_df+1))
news_df = news_df.reset_index()

df_idf = pd.DataFrame()
df_idf['Word'] = news_df['word']
df_idf['idf'] = list(idf['count1'])
#df_idf = df_idf.sort_values('idf', ascending=False)

#df_idf.to_csv('/df_idf.csv', encoding="utf-8-sig")

# TF-IDF (Term Frequency-Inverse Document Frequency)
tf = pd.read_csv('/news_tf.csv')
idf = pd.read_csv('/df_idf.csv')

#tf와 idf index가 다르기때문에, 둘다 가지고 있는 값만 계산 할 것임
del tf['Unnamed: 0']
del idf['Unnamed: 0']

news_tf.columns = ["Word","tf"]
df_tfidf = pd.merge(news_tf,df_idf, on = "Word")
df_tfidf["tfidf"] = df_tfidf["tf"] * df_tfidf["idf"]
df_tfidf.to_csv('/tfidf.csv', encoding="utf-8-sig")
