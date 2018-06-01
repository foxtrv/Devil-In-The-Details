# Devil In The Details
An original idea I had based off of the idiom ["The devil is in the detail"](https://en.wikipedia.org/wiki/The_devil_is_in_the_detail)

Is the Devil truly in the details? I wanted to find out.

# What I Did

Using Dante's Inferno by Dante Alighieri as reference, I downloaded a pdf I found online and scraped the contents to a text file.

I then used a Sentiment Analysis API I found at http://text-processing.com to compute the sentiment on the original body of text versus an NLTK summarized version of the text (summarized 10x fold) using code I stole from https://glowingpython.blogspot.com/2014/09/text-summarization-with-nltk.html. 

(I had to average the score for the original text as the API limits sentiment analysis to 50,000 characters at a time)

# Conclusion
In conclusion, I found that the Devil is not in the details. 
(However, Dante's Inferno is written in poem and sometimes it's even hard for me to understand the sentiment of what he is saying lol)


