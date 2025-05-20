import praw
import re
from collections import defaultdict
import json
import os
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from urllib.parse import urlparse

reddit = praw.Reddit(client_id =os.getenv("CLIENT_ID"), 
					client_secret =os.getenv("CLIENT_SECRET"), 
					user_agent ='trend_topics')

# Stopwords básicas 
stopwords = {
    'the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'that', 'for', 'on', 'was',
    'with', 'he', 'she', 'you', 'this', 'are', 'as', 'be', 'have', 'but', 'not',
    'at', 'by', 'from', 'or', 'an', 'they', 'we', 'his', 'her', 'their', 'has',
    'i', 'me', 'my', 'myself', 'your', 'what', 'which', 'who', 'them', 'if',
    'would', 'so', 'like', 'just', 'more', 'about', 'when', 'some', 'can', 'how',
    'any','https','please','only','subreddit','reddit','here'
}

def get_top_words(subreddit_url, n=20):
    # Extrai o nome do subreddit da URL
    subreddit_name = urlparse(subreddit_url).path.split('/')[2]
    subreddit = reddit.subreddit(subreddit_name)
    
    word_counts = defaultdict(int)

    with open ("words.txt","w+") as text_file:
        # analisa os comentários mais recentes
        for comment in subreddit.comments(limit=None):
            words = re.findall(r'\b[a-z]{3,}\b', comment.body.lower())

            filtered_words = [word for word in words if word not in stopwords]

            for word in filtered_words:
                text_file.write(word + " ")
                word_counts[word] += 1
        
        # ordena e retorna as N palavras mais frequentes
        top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:n]
        return json.dumps(dict(top_words), indent=4)
    
def get_word_cloud():
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    text = open(path.join(d, 'words.txt')).read()

    wordcloud = WordCloud().generate(text)

    plt.imshow(wordcloud, interpolation='bilinear',cmap='viridis')
    plt.colorbar()
    plt.title("Nuvem de Palavras")
    plt.savefig("wordcloud.png")



json_result = get_top_words("https://www.reddit.com/r/skincancer/", n=20)
get_word_cloud()
print(json_result)