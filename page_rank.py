
# coding: utf-8

# In[1]:


#Name: Sandeep Rane
#Netid: srane3
#UIN: 677515266


# In[2]:


import nltk, os, re, math, string
from nltk import PorterStemmer
from pathlib import Path


# In[3]:


dirPath = Path(input('Enter the path to the abstracts dataset directory/folder: '))
goldPath = Path(input('Enter the path to the gold dataset directory/folder: '))
stopwordPath = Path(input('Enter the path to the stopwords file: '))
wSize = int(input('Enter the size of the window "w": '))

#dirPath = 'www/abstracts' 
#goldPath = 'www/gold'
#stopwordPath = 'stopwords.txt'


# In[4]:


stopword_list = []
topK_Ngrams_File = {}
goldFile = {}
rankSum = {}

stemmer = PorterStemmer()


# In[5]:


class graphNode():
    def __init__(self, word):
        self.word = word
        self.edges = {}
        self.score = 0
        self.timesAdj = 0
    def addEdge(self, word):
        if word not in self.edges:
            self.edges[word] = 1
        else:
            self.edges[word] += 1
        self.timesAdj += 1


# In[6]:


def parseStopwords():
    file_object = open(stopwordPath, 'r')
    for aStopword in file_object:
        aStopword = aStopword.lower()
        aStopword = re.split("\n",aStopword)
        stopword_list.append(aStopword[0])
    file_object.close()


# In[7]:


def tokenizer(file_content):
    file_content = file_content.lower()
    generatedTokens = file_content.split()
    return generatedTokens


# In[8]:


def tagSeparator(token):
    tags = ['_nn', '_nns', '_nnp', '_nnps', '_jj']
    if token[-3:] in tags:
        return token[:-3], token[-2:]
    elif token[-4:] in tags:
        return token[:-4], token[-3:]
    elif token[-5:] in tags:
        return token[:-5], token[-4:]
    else:
        return '',''


# In[9]:


def stemAndCheck(aToken):
    if aToken in stopword_list:
        return ''
    stemWord = stemmer.stem(aToken)
    if stemWord not in stopword_list:
        return stemWord
    return ''


# In[10]:


def addToGraph(graph_words, wordList):
    nodes = []
    for word in wordList:
        if word != '':
            nodes.append(word)
            if word not in graph_words:
                graph_words[word] = graphNode(word)
    for i in range(len(nodes)-1):
        for j in range(i+1, len(nodes)):
            graph_words[nodes[i]].addEdge(nodes[j])
            graph_words[nodes[j]].addEdge(nodes[i])
    #print(nodes)
    #for i in graph_words:
    #    print(graph_words[i].word, graph_words[i].timesAdj)


# In[11]:


def computePageRank(graph_words):
    dF = 0.85
    n = 10
    v = len(graph_words)
    for word, wordNode in graph_words.items():
        wordNode.score = 1/v
    for i in range(n):
        wordScores = {}
        for word, wordNode in graph_words.items():
            if len(wordNode.edges) != 0:
                temp = 0
                for vj, wji in wordNode.edges.items():
                    temp += (wji * graph_words[vj].score) / graph_words[vj].timesAdj
                wordScores[word] = (dF*temp) + ((1-dF)*(1/v))
        for w,s in wordScores.items():
            graph_words[w].score = s


# In[12]:


def topK_Ngrams(uGram, bGram, tGram, graph_words):
    scoreNgrams = []
    for word in uGram:
        score = graph_words[word].score
        scoreNgrams.append((score, word))
    for words in bGram:
        score = graph_words[words[0]].score + graph_words[words[1]].score
        word = words[0] + ' ' + words[1]
        scoreNgrams.append((score, word))
    for words in tGram:
        score = graph_words[words[0]].score + graph_words[words[1]].score + graph_words[words[2]].score
        word = words[0] + ' ' + words[1] + ' ' + words[2] 
        scoreNgrams.append((score, word))
    return sorted(scoreNgrams, reverse = True)[:10]


# In[13]:


def preprocessGold(file_content):
    phrases = []
    for phrase in file_content:
        phrase = phrase.split()
        res = ''
        for word in phrase:
            pWord = stemmer.stem(word)
            res += pWord + ' '
        phrases.append(res[:-1])
    return phrases


# In[14]:


def findRank(topK_Ngrams, goldFile):
    i = 0
    for score, phrase in topK_Ngrams:
        i += 1
        if phrase in goldFile:
            return 1/i
    return 0


# In[15]:


def readDatasetAndCompute():
    doc_count = 0
    file_ranks = []
    for x in os.listdir(dirPath):
        graph_words = {}
        uGram = {}
        bGram = {}
        tGram = {}
        prevWord = ''
        prevPrevWord = ''
        wordList = []
        if x not in os.listdir(goldPath):
            continue
        doc_count += 1
        filename = dirPath / x
        file_content = filename.read_text()
        tokens = tokenizer(file_content)
        for aToken in tokens:
            word, tag = tagSeparator(aToken)
            word = stemAndCheck(word)
            wordList.append(word)
            if word != '' and word not in uGram:
                uGram[word] = 0
            if prevWord != '' and word != '':
                bGram[(prevWord, word)] = 0
                if prevPrevWord != '':
                    tGram[(prevPrevWord, prevWord, word)] = 0
            if len(wordList) == wSize:
                addToGraph(graph_words, wordList)
                wordList = []
            prevPrevWord = prevWord
            prevWord = word
        if len(wordList) != 0:
            addToGraph(graph_words, wordList)
            wordList = []
        computePageRank(graph_words)
        topK_Ngrams_File[x] = topK_Ngrams(uGram, bGram, tGram, graph_words)
        filename = goldPath / x
        file_content = (filename.read_text()).splitlines()
        goldFile[x] = preprocessGold(file_content)
        rank_rd = findRank(topK_Ngrams_File[x], goldFile[x])
        #print(rank_rd)
        file_ranks.append(rank_rd)
    for i in range(1,11):
        rankSum[i] = 0
    for j in file_ranks:
        if j == 0:
            continue
        for i in range(1,11):
            if (j**-1) <= i:
                rankSum[i] += j
    print('\nThe computed MRR@k values for w=' + str(wSize) + ' are: \n')
    for i in range(1,11):
        rankSum[i] = rankSum[i]/doc_count
        print('At k = ' + str(i) + ': ' + str(rankSum[i]))


# In[16]:


parseStopwords()


# In[17]:


readDatasetAndCompute()

