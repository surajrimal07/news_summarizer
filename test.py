import requests
from extractnet import Extractor


raw_html = requests.get('https://apnews.com/article/6e58b5742b36e3de53298cf73fbfdf48').text
results = Extractor().extract(raw_html)
for key, value in results.items():
    print(key)
    print(value)
    print('------------')