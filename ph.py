import requests
import json
from bs4 import BeautifulSoup

response = requests.get('https://www.pornhub.com/view_video.php?viewkey=ph5e6e8dfda1396')

soup = BeautifulSoup(response.text,'html.parser')
seo_json = soup.find('script',{'type':'application/ld+json'}).string
data = json.loads(seo_json)
print(data)

from db import Video

video = Video(
    title=data['name']
    
)