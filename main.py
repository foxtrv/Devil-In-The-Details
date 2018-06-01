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
def sentimentAnalysis(text, dict):
    # print('\033[31m' + '=== PERFORMING SENTIMENT ANALYSIS ===' + '\033[30m')
    data = [
        ('text', text),
    ]
    response = requests.post('http://text-processing.com/api/sentiment/', data=data)
    data = json.loads(str(response.json()).replace('\'', '"'))
    label = str(data['label'])
    # printing for debugging purposes
    # print('pos: ' + str(data['probability']['pos']))
    # print('neg: ' + str(data['probability']['neg']))
    # print('neutral: ' + str(data['probability']['neutral']))
    # print('label: ' + label)
    dict['pos'] += data['probability']['pos']
    dict['neg'] += data['probability']['neg']
    dict['neutral'] += data['probability']['neutral']
    dict['label'].append(label)
    dict['numTimesUpdated'] += 1


# followed guide found here: https://web.archive.org/web/20140821083738/http://nltk.googlecode.com/svn/trunk/doc/book/book.html
def summarizeText(text):
    # print('\033[35m' + 'PERFORMING TEXT SUMMARIZATION...' + '\033[30m')
    fs = FrequencySummarizer()
    sum = ''
    # summarize text by factor of 10
    for s in fs.summarize(text, math.ceil(len(text.splitlines()) / 10)):
        sum += s
    file = open('out.txt', 'w')
    file.write(sum)
    file.close()
    return sum


def main():
    # f = convertPDFToText('Dante-s-Inferno.pdf', 'di.txt') # already ran this, don't need to run it again
    file = open('di.txt', 'r')

    dict = {"pos": 0,
            "neg": 0,
            "neutral": 0,
            "label": [],
            "numTimesUpdated": 0}

    # sentimentAnalysis API limit is 50,000 characters
    textLimited = ''
    for line in file:
        for c in line:
            if (len(textLimited) > 0 and len(textLimited) % 50000 == 0):
                sentimentAnalysis(textLimited, dict)
                textLimited = ''
            else:
                textLimited += c

    posTotal = dict['pos'] / dict['numTimesUpdated']
    negTotal = dict['neg'] / dict['numTimesUpdated']
    neutralTotal = dict['neutral'] / dict['numTimesUpdated']

    # printing for debugging purposes
    # print('\033[35m' + "=== Original Length Text Analysis ===" + '\033[30m')
    # print("number of text segments: " + str(dict['numTimesUpdated']))
    # print("pos: " + str(posTotal))
    # print("neg: " + str(negTotal))
    # print("neutral: " + str(neutralTotal))

    labelTotal = max(posTotal, negTotal, neutralTotal)
    originalLabel = ""
    stringOut = "label for original length text is: "
    if (labelTotal == posTotal):
        print(stringOut + "positive")
        originalLabel = "positive"
    elif (labelTotal == negTotal):
        print(stringOut + "negative")
        originalLabel = "negative"
    elif (labelTotal == neutralTotal):
        print(stringOut + "neutral")
        originalLabel = "neutral"

    s = summarizeText(textLimited)

    dict = {"pos": 0,
            "neg": 0,
            "neutral": 0,
            "label": [],
            "numTimesUpdated": 0}

    sentimentAnalysis(s, dict)
    sumLabel = dict['label'][0]
    print("label for summarized text is: " + sumLabel)

    if (originalLabel != sumLabel):
        print("Yes, the devil is in the details")
    else:
        print("No, the devil is not in the details")


if __name__ == "__main__":
    main()
