from array import *
from nltk.corpus import stopwords


def get_corpus(data):
    corpus = []
    for phrase in data:
        for word in phrase.split():
            corpus.append(word)
    return corpus

def str_corpus(corpus):
    str_corpus = ''
    for i in corpus:
        str_corpus += ' ' + i
    str_corpus = str_corpus.strip()
    return str_corpus


Text1=open('text1.txt', 'rt',encoding='utf8')
text1=get_corpus(Text1)
Text2=open('text2.txt', 'rt',encoding='utf8')
text2=get_corpus(Text2)
text1 = list(map(lambda x: x.lower(), text1))
text2 = list(map(lambda x: x.lower(), text2))
print(text1)
print(text2)

strin1=str_corpus(text1)
strin2=str_corpus(text2)
a=len(text1)
b=len(text2)
num_words1 = len(set(text1))
num_words2 = len(set(text2))
num=num_words1+num_words2


for i in range (a):
    for j in range(i+1,a):
        if text1[i]==text1[j] or text1[i]=="":
            text1[j]=""
    if text1[i] in stopwords.words('russian'):
        text1[i]=""
    if text1[i]=="." or text1[i]=="-" or text1[i]=="?" or text1[i]=="!" or text1[i]=="...":
            text1[i]=""
i=0

# while text1[i] != None :
#     if text1[i] =="":
#         text1.pop(i)

for i in range (b):
    for j in range(i+1,b):
        if text2[i]==text2[j]:
            text2[j]=""
    if text2[i] in stopwords.words('russian'):
        text2[i]=""
    if text2[i]=="." or text2[i]=="-" or text2[i]=="?" or text2[i]=="!" or text2[i]=="...":
        text2[i]=""

print(text1)
print(text2)
Z=0
for i in range (a):
    for j in range(b):
        if text1[i]==text2[j] and text1[i]!="":
            print('Есть совпадение '+str(i) + " " + str(j)+ " " + text1[i])
            num=num-1
            Z=Z+1

print("Количество уникальных слов "+ str(num))
perc=(Z/num)*100
print("Процент совпадения "+ str(perc)+"%")
if perc>10:
    print("Тексты об одном и том же")
else:
    print("Не об одном и том же")
