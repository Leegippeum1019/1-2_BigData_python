import pandas as pd
import glob
import re
import nltk

from functools import reduce
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS, WordCloud

#nltk.download()

all_files = glob.glob('C:/Users/LG/Desktop/빅데이터_파이썬/5_data/myCabinetExcelData*.xls')
#print(all_files) #출력하여 내용 확인

all_files_data = [] #전체 데이터를 저장할 리스트
for file in all_files:
    data_frame = pd.read_excel(file)
    all_files_data.append(data_frame)
#print(all_files_data[0]) #첫번째 csv 파일에 있는 데이터 출력

all_files_data_concat = pd.concat(all_files_data, axis = 0, ignore_index = True)
#print(all_files_data_concat) #1,000개 데이터 출력하여 내용 확인

all_files_data_concat.to_csv('riss_bigdata.csv', encoding='utf-8-sig', index = False)

all_title = all_files_data_concat['제목']
#print(all_title) #출력하여 1,000개 데이터의 제목 확인

stopWords = set(stopwords.words("english")) #영어 불용어를 불러와서 저장
lemma = WordNetLemmatizer()

words = []

for title in all_title:
    EnWords = re.sub(r"[^a-zA-Z]+"," ",str(title)) #알파벳 이외의 값은 공백으로 대체
    EnWordsToken = word_tokenize(EnWords.lower()) #위의 결과 str을 소문자로 바꾼 뒤, 토큰화
    EnWordsTokenStop = [w for w in EnWordsToken if w not in stopWords] #불용어 제거
    EnWordsTokenStopLemma = [lemma.lemmatize(w) for w in EnWordsTokenStop] #표제어 추출
    words.append(EnWordsTokenStopLemma)

words2 = list(reduce(lambda x, y: x + y, words))
#print(words2)

count = Counter(words2) #word2 리스트에 있는 단어 별로 빈도 수를 계산하여 결과로 딕셔너리 생성
#print(count)

word_count = dict()
for tag, counts in count.most_common(50): #출현 횟수가 많은 상위 50개 단어 추출
    if (len(str(tag))>1):
        word_count[tag] = counts
        #print("{} : {}".format(tag,counts))


del word_count['big']
del word_count['data']

plt.bar(range(len(word_count)), word_count.values(), align='center')
plt.xticks(range(len(word_count)),word_count.keys(), rotation='vertical')
plt.show()

all_files_data_concat['doc_count'] = 0
summary_year = all_files_data_concat.groupby('출판일', as_index=False)['doc_count'].count()
print(summary_year)

plt.figure(figsize = (12, 5))
plt.xlabel('year')
plt.ylabel('doc-count')
plt.grid(True)
plt.plot(range(len(summary_year)), summary_year['doc_count'])
plt.xticks(range(len(summary_year)), summary_year['출판일'])
plt.show()

stopwords = set(STOPWORDS)
wc = WordCloud(background_color = 'ivory',
               stopwords=stopwords,
               width = 800,
               height = 600)
cloud = wc.generate_from_frequencies(word_count)
plt.figure(figsize = (8,8))
plt.imshow(cloud)
plt.axis('off')
plt.show()