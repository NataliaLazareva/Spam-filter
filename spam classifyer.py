# -*- coding: utf-8 -*-

import glob
import numpy as np
import math

DictionaryForHam = {}
DictionaryForSpam = {}

def message_filter(ch):

    symbols = ['!','@','&','#','$','%', '?', '.', '+', '{', '}', '(', ')','[', ']', '^', '*', '=', '/', '|' ]

    for c in ch:
        for h in c:
           if (h in symbols):
              return False
           else:
              return True
 
def file_open(file):
    f = open(file, 'r', encoding = "ISO-8859-1")
    text = f.read()
    text = text.lower()
    f.close()
    words = text.split()
    words1 = filter(message_filter, words)
    return words1

#Получение списка файлов для класса спам и неспам
ham_path = glob.glob('C:\\users\\DELL\\Desktop\\folder\\enron*\\ham\\*.txt')
spam_path = glob.glob('C:\\users\\DELL\\Desktop\\folder\\enron*\\spam\\*.txt')

#Разделение на Test и Train
ham_max = np.int32(len(ham_path)*0.75)
spam_max = np.int32(len(spam_path)*0.75)
ham_training = ham_path[:ham_max]
spam_training = spam_path[:spam_max]
ham_testing = ham_path[ham_max:]
spam_testing = spam_path[spam_max:]

#Процесс тестирования
filter_words = []

for file in ham_training:
    words1 = file_open(file)

    for word in words1:
        if word in DictionaryForHam.keys():
            DictionaryForHam[word]+=1
        else: DictionaryForHam[word]=1
    filter_words += words1

for file in spam_training:
    words1 = file_open(file)

    for word in words1:
        if word in DictionaryForSpam.keys():
            DictionaryForSpam[word]+=1
        else: DictionaryForSpam[word]=1
    filter_words += words1

ListOfUniqueWords = set(filter_words)
print(ListOfUniqueWords)

#Конечные параметры
D_0 = len(ham_training)
D_1 = len(spam_training)
R = D_0 + D_1
V = len(ListOfUniqueWords)
F_c0 = sum(DictionaryForHam.values())
F_c1 = sum(DictionaryForSpam.values())  

#Процесс тестирования
C_inHam = 0
C_inSpam = 0
HamTestingResults = []
SpamTestingResults = []

for file in ham_testing:
    words1 = file_open(file)
    C_00 = math.log(D_0/R)
    C_01 = C_00
    for word in words1:
        C_00+=(DictionaryForHam[word]+1)/(V+F_c0)
        C_01+=(DictionaryForSpam[word]+1)/(V+F_c1)

    if C_00>C_01: 
        HamTestingResults.append(0)
    else: 
        HamTestingResults.append(1)
   
for file in spam_testing:
    words1 = file_open(file)
    C_10 = math.log(D_1/R)
    C_11 = C_10
    for word in words1:
        C_10+=(DictionaryForHam[word]+1)/(V+F_c0)
        C_11+=(DictionaryForSpam[word]+1)/(V+F_c1)
    
    if C_10>C_11: 
        SpamTestingResults.append(0)
    else: 
        SpamTestingResults.append(1)