import requests
from readability import Document
import re

# clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

# response = requests.get('https://www.bizshala.com/article/6042')
# document = Document(response.content)
# #doc = document.title()
# elem = document.summary()
# data = re.sub(clean,'',elem)

from newspaper import Article

url = 'https://www.sharesansar.com/newsdetail/nepal-and-ireland-discuss-educational-collaboration-for-quality-advancements-2024-01-11'

lan = 'en'

if 'merolagani' in url:
    lan = 'hi'

article = Article(url, language=lan)
article.download()

article.parse()

if lan == 'en':
    article.nlp()
    print(article.summary)
else:
    print(article.text)