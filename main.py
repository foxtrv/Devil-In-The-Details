import json

import PyPDF2
import math
import requests

from FrequencySummarizer import FrequencySummarizer


def convertPDFToText(pdf, nameOfOutputFile):
    file = open(pdf, 'rb')
    fileReader = PyPDF2.PdfFileReader(file)
    text = ''
    for i in range(fileReader.getNumPages()):
        page = fileReader.getPage(i)
        text += page.extractText()
    file = open(nameOfOutputFile, 'w')
    file.write(text)
    file.close()


# using Sentiment Analysis API found at http://text-processing.com
def sentimentAnalysis(text):
    print('\033[31m' + '=== PERFORMING SENTIMENT ANALYSIS ===' + '\033[30m')
    data = [
        ('text', text),
    ]
    response = requests.post('http://text-processing.com/api/sentiment/', data=data)
    data = json.loads(str(response.json()).replace('\'', '"'))
    print('pos: ' + str(data['probability']['pos']))
    print('neg: ' + str(data['probability']['neg']))
    print('neutral: ' + str(data['probability']['neutral']))
    label = str(data['label'])
    if (label == 'neutral'):
        print('label: ' + '\033[90m' + label + '\033[30m')
    elif (label == 'pos'):
        print('label: ' + '\033[32m' + label + '\033[30m')
    elif (label == 'neg'):
        print('label: ' + '\033[31m' + label + '\033[30m')


# followed guide found here: https://web.archive.org/web/20140821083738/http://nltk.googlecode.com/svn/trunk/doc/book/book.html
def summarizeText(text):
    print('\033[35m' + '=== PERFORMING TEXT SUMMARIZATION ===' + '\033[30m')
    fs = FrequencySummarizer()
    sum = ''
    # summarize text by factor of 10
    # for s in fs.summarize(text, math.ceil(len(text.splitlines())/10)):
    for s in fs.summarize(text, math.ceil(len(text.splitlines()) / 10)):
        sum += s
    file = open('out.txt', 'w')
    file.write(sum)
    file.close()
    return sum


def main():
    # f = convertPDFToText('Dante-s-Inferno.pdf', 'di.txt') # already ran this, don't need to run it again
    file = open('di.txt', 'r')

    # sentimentAnalysis API limit is 50,000 characters
    textLimited = ''
    for line in file:
        for c in line:
            if (len(textLimited) >= 50000):
                break
            textLimited += c

    sentimentAnalysis(textLimited)
    print('\nlength of regular text = ' + str(len(textLimited)) + '\n')

    s = summarizeText(textLimited)
    print('\nlength of summarized text = ' + str(len(s)) + '\n')

    sentimentAnalysis(s)


if __name__ == "__main__":
    main()
