import os
import re
import string
from numpy import positive
import syllables
from nltk.tokenize import word_tokenize,sent_tokenize


class Analyze:
    
    # Read the text file 
    def getTextFromFile(self,fileName):
        file = open(f"textFiles/{fileName}.txt","rb")
        textToProcess = ' '.join(map(str, file.readlines()))
        file.close()
        #print(textToProcess)
        return textToProcess
    
    # Read all the stop words available in text file
    def stopWords(self):
        directory = 'StopWords'
        finalListOfStopWords = []
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                file = open(f, "r", encoding = "ISO-8859-1")
                #print(file.readlines())
                finalListOfStopWords = finalListOfStopWords + file.readlines()
                file.close()
        finalListOfStopWords = list(map(str.strip,finalListOfStopWords))
        return finalListOfStopWords

    # Create Sentence Token
    def sentenceToken(self,textToProcess):
        sentenceToken = sent_tokenize(textToProcess)
        return sentenceToken

    # Create Word Token and remove the punctuation
    def wordToken(self,textToProcess):
        #Remove punctuation 
        textToProcess = textToProcess.translate(textToProcess.maketrans('', '', string.punctuation))
        return word_tokenize(textToProcess)
        
    # Remove all the stop Words
    def removeStopWords(self, textTokens, finalListOfStopWords):
        textTokensWithoutSW = [word for word in textTokens if not word in finalListOfStopWords]
        return textTokensWithoutSW

    # Get all the positive Words
    def positiveWords(self, cleanData):
        file = open("MasterDictionary/positive-words.txt", "r")
        positiveWordList = list(map(str.strip, file.readlines()))
        file.close()
        positiveWordsInArticle = [word for word in cleanData if word in positiveWordList]
        return positiveWordsInArticle

    #Get all the negative Words
    def negativeWords(self,cleanData):
        file = open("MasterDictionary/negative-words.txt", "r")
        negativeWordList = list(map(str.strip, file.readlines()))
        file.close()
        negativeWordsInArticle = [word for word in cleanData if word in negativeWordList]
        return negativeWordsInArticle


    # Get complex Words
    def complexWords(self, cleanData):
        words = ([word for word in cleanData if not word.endswith('es') or word.endswith('ed')])
        complexWords = []
        totalSyllable = 0
        for word in enumerate(words):
            totalSyllable = totalSyllable + syllables.estimate(str(word))
            if syllables.estimate(str(word)) > 2:
                complexWords.append(word)
        data = {"complexWords": len(complexWords),"totalSyllable": totalSyllable}
        return data

    # Get personal Pronouns
    def personalPronouns(self,textToProcess):
        pronounRegex = re.compile(r'\b(I|we|my|ours|(?-i:us))\b',re.I)
        pronouns = pronounRegex.findall(textToProcess)
        return pronouns

    def returnAllAnalysedData(self,fileName):
        textData = self.getTextFromFile(fileName)
        cleanDataList = self.removeStopWords(self.wordToken(textData), self.stopWords())
        analysedData = {
            "sentenceCount": len(self.sentenceToken(self.getTextFromFile(fileName))),
            "wordCount": len(cleanDataList),
            "positiveScore": len(self.positiveWords(cleanDataList)),
            "negativeScore": len(self.negativeWords(cleanDataList)),
            "polarityScore": (len(self.positiveWords(cleanDataList)) - len(self.negativeWords(cleanDataList)) )/((len(self.positiveWords(cleanDataList)) + len(self.negativeWords(cleanDataList))) + 0.000001),
            "subjectiveScore": (len(self.positiveWords(cleanDataList)) - len(self.negativeWords(cleanDataList))) / (len(cleanDataList) + 0.000001 ) ,
            "avgSentenceLength": len(cleanDataList)/len(self.sentenceToken(self.getTextFromFile(fileName))),
            "avgNoOfWoordsPerSentence": len(cleanDataList)/len(self.sentenceToken(self.getTextFromFile(fileName))),
            "avgWordLength": (sum(len(word) for word in cleanDataList))/len(cleanDataList),
            "countofComplexWords": self.complexWords(cleanDataList)['complexWords'],
            "totalSyllable": self.complexWords(cleanDataList)['totalSyllable'],
            "%OfComplexWords": self.complexWords(cleanDataList)['complexWords'] / len(cleanDataList) ,
            "fogIndex": 0.4*((len(cleanDataList)/len(self.sentenceToken(self.getTextFromFile(fileName)))) + (self.complexWords(cleanDataList)['complexWords']/len(cleanDataList)) ),
            "personalPronounsCount": len(self.personalPronouns(textData))
        }
        return analysedData
        
        