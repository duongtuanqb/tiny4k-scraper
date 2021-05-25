from mongoengine.errors import DoesNotExist, NotUniqueError
import requests
from bs4 import BeautifulSoup
import urllib.parse
import utilities
import db
import gDriveLib
import random
import os

DOMAIN = 'https://members.tiny4k.com'
COOKIE = '_ga=GA1.2.1477273752.1621924268; _gid=GA1.2.1107768605.1621924268; CloudFront-Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNjIyMDEwOTQwfX19XX0_; CloudFront-Signature=eGD5vRvRTuIVgJ3jLq1eWnBZ5DPn2RwQ1UvosiCB5glzescJLGAKN~0VzZMeBXX9l2JY2rb65vATazq9Jrnl32aaPAWFFJs5-r5umzr72huk1kao4ucitmPWTqtwxEtnnmaCQuhBr~Uqb6hk~OaLX9FwzNvGqFyl52Dv~duHNvT9HbezopCn4W6rHWY~tw2FgeqSu6mwdjvhl1pWiSIhiFGRIUQvabORMhacKvgk0Nk6GNhYKCFSC3ajLe~dvF5sha7YTalLPevh3MNvSxRs03zA9c3iIIooHcSYJbLrBjmdmUz43zjUXMPiuFDcQ-Sd4acd3CsaAxrOX9oqHHckfA__; CloudFront-Key-Pair-Id=APKAI76GCCLZDPHFI5AQ; l=vt52Ailj1wTP38dkGyZGXA%3D%3D; i=PPcaqhrZ_HpWLILQx-I2hbxbqixZxvYtluiMgSStAVI%3D; u=9hOL8pn-nbZ5WKoq_hvaVw%3D%3D; c=aTj71oZVTQrwMNwyR11bJw%3D%3D; b=kuf0E01uq0WaDJ-a1HcAlQ%3D%3D; j=FJxVwz9mwipa0cw6kW10qQrKPZBzDLiIHfvdglUhO2U%3D; _vip_session=bHVja3k%3D%0A--ifUsyUC0wfZY8eOwzwe8YAZ092vu2LFUscCP0fwqwZE%3D'
DRIVE = '1xax_5cvxHUFLylCil7JYqWVA_64dCWF1'
TEAM_DRIVE = '0ACtX2h760dS3Uk9PVA'

try:
    studio = db.Studio(name='Tiny4K')  
    studio.save()
except NotUniqueError:
    pass


class Video:
    def __init__(self, url):
        print(f'scraping {url}')
        self.url = url
        self.original_url = url
        self.proxies = utilities.getProxy()
        self.getPage()
        self.getInfo()
        self.getStreams()
        self.getScreencaps()
        self.getPictures()
        self.uploadDrive()

    def save(self):
        video = db.Video(
            title = self.title,
            url = self.original_url,
            thumbnail = random.choice(self.screencaps),
            studio = db.Studio.objects.get(name='Tiny4K'),
            actors = self.actors,
            screencaps = self.screencaps,
            pictures = self.pictures,
            drive = self.drive,
            slug = utilities.generateSlug(self.title)
        )
        video.save()
        return video

    def uploadDrive(self):
        try:
            self.file_name = utilities.randomName()+'.mp4'
            utilities.download(self.videos[-1]['url'],self.file_name,COOKIE)
            file_id = gDriveLib.upload(self.file_name,self.title+'.mp4',DRIVE,TEAM_DRIVE)
            os.remove(self.file_name)
            self.drive = file_id
        except Exception as e:
            os.remove(self.file_name)
            raise e

    def getPage(self):
        response = requests.get(url=self.url,
                                headers={
                                    'cookie': COOKIE
                                },proxies=self.proxies)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.source = soup

    def getInfo(self):
        info_div = self.source.find('div', {'class': 'release-info'})
        self.title = info_div.find('h1', {'class': 'title'}).string
        actors = info_div.find_all('a', {'class': 'actor-title'})
        self.actors = []
        for i in actors:
            try:
                new_actor = db.Actor(name=i.string).save()
            except NotUniqueError:
                new_actor = db.Actor.objects.get(name=i.string)
            self.actors.append(new_actor)


    def getStreams(self):
        download_div = self.source.find('div', {'class': ['col', 'dropdown']}).find(
            'div', {'class': ['dropdown-menu', 'w-100']})
        qualities = download_div.find_all('a', {'class': 'dropdown-item'})
        videos = []
        for vid in qualities:
            if not DOMAIN in vid['href']:
                url = urllib.parse.urljoin(DOMAIN, vid['href'])
            else:
                url = vid['href']
            params = dict(urllib.parse.parse_qsl(
                urllib.parse.urlsplit(url).query))
            filename = params['filename']
            if '2160' in filename:
                res = 2160
            if '1080' in filename:
                res = 1080
            if '720' in filename:
                res = 720
            if '480' in filename:
                res = 480
            if '360' in filename:
                res = 360
            if '240' in filename:
                res = 240
            extension = filename.split('.')[-1]
            if res < 2160:
                videos.append({
                    'url': url,
                    'filetype': extension,
                    'filename': filename,
                    'res': res
                })
        self.videos = utilities.sortList(videos, 'res')

    def getScreencaps(self):
        self.url = self.original_url+'/'+'screencaps'
        self.getPage()
        imgs = self.source.find_all('img', {'class': 'thumbnail'})
        self.screencaps = []
        for img in imgs:
            try:
                new_image = db.Image(
                    url=img['fullsrc'],
                    preview_url=img['data-src']
                ).save()
            except NotUniqueError:
                new_image = db.Image.objects.get(url=img['fullsrc'])
            self.screencaps.append(new_image)


    def getPictures(self):
        self.url = self.original_url+'/'+'pictures'
        self.getPage()
        imgs = self.source.find_all('img', {'class': 'thumbnail'})
        self.pictures = []
        for img in imgs:
            try:
                new_image = db.Image(
                    url=img['fullsrc'],
                    preview_url=img['data-src']
                ).save()
            except NotUniqueError:
                new_image = db.Image.objects.get(url=img['fullsrc'])
            self.pictures.append(new_image)



class Crawl:
    def __init__(self):
        self.url = 'https://members.tiny4k.com/scenes?sort=latest&page='
        self.page = 1
        while True:
            self.getPage()
            print(f'crawling {self.url}{self.page}')
            links = self.getLinks()
            if len(links) <1:
                break
            for i in links:
                url = urllib.parse.urljoin(DOMAIN,i['href'])
                try:
                    new_task = db.Task(url=url,processed=False)
                    new_task.save()
                except NotUniqueError:
                    pass
            else:
                self.page +=1

    def getPage(self):
        response = requests.get(url=self.url+str(self.page),
                        headers={
                            'cookie': COOKIE
                        },
                        proxies=utilities.getProxy())
        soup = BeautifulSoup(response.text, 'html.parser')
        self.source = soup
        print(self.source)

    def getLinks(self):
        links = self.source.find_all('a',{'class' : 'video-title'})
        return links


# video = Video('https://members.tiny4k.com/video/bubbly-spinner')
# video.save()

