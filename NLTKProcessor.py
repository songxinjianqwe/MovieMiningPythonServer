# coding=utf-8
import nltk
import os
from collections import Counter
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import re
import json


def cutWords(reviewContent):
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sents = sent_tokenizer.tokenize(reviewContent.lower())  # 小写，并分句
    words = []
    for sent in sents:
        words.extend(nltk.word_tokenize(sent))  # 分词
    stopwords = nltk.corpus.stopwords.words("english")
    english_punctuations = [',', '.', ':', '', '?', '(', ')', '[', ']', '!', '@', '#', '%', '$', '*', '=', 'abstract=',
                            '{', '}', '\'', '"']
    bannedWords = []
    for line in open("BannedWords.txt").readlines():
        bannedWords.extend(line.split())
    resultWords = []
    for word in words:
        if word not in stopwords:  # 去掉停用词
            if word not in english_punctuations:  # 去掉标点符号
                if len(word) >= 3:  # 去掉长度小于等于2的单词
                    if not word.isdigit():  # 去掉全为数字的单词
                        if word not in bannedWords:  # 去掉自定义停用词
                            stemWord = nltk.corpus.wordnet.morphy(word)
                            if stemWord is not None:
                                resultWords.append(stemWord)  # 获取词干
    return resultWords

def findKeyWords(reviewContent, topN):
    return [key[0] for key in Counter(cutWords(reviewContent)).most_common(topN)]


def calcKeyWords(baseDir, topN,returnFileLoc):
    pattern = re.compile(r"comment_(.*?).txt")
    files = os.listdir(baseDir)
    contents = []
    for file in files:
        contents.append(open(os.path.join(baseDir, file)).readline())
    # print(contents)
    vectorizer = CountVectorizer()
    # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()
    # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(contents))
    # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    words = vectorizer.get_feature_names()
    # 获取词袋模型中的所有词语
    weight = tfidf.toarray()
    # 将tf-idf矩阵抽取出来，元素weight[i][j]表示j词在i类文本中的tf-idf权重
    result = {}
    for i in range(len(weight)):
        # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for遍历某一类文本下的词语权重
        print("第 %d 类文本" % i)
        wordWight = []
        for j in range(len(words)):
            word = words[j]
            value = weight[i][j]
            wordWight.append((word, value))
        midResult = sorted(wordWight, key=lambda tuple: tuple[1], reverse=True)
        result[pattern.findall(os.path.basename(files[i]))[0]] = [key[0] for key in midResult[:topN]]
        # print(result)
    jsonStr = json.dumps(result)
    open(returnFileLoc, "w").write(jsonStr)



if __name__ == "__main__":
    # print(findKeyWords(open("E:/test_comments/comment_0782002064.txt").readline(), 5))
    calcKeyWords("E:/comments/", 5)
