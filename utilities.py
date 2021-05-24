import requests
from tqdm import tqdm
import os
import random
import string
import json

def randomName(length=10):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def sortList(unsort,key):
    return sorted(unsort,key=lambda obj: obj[key])

def download(url, dst, cookie=None,chunk_size=1024*1024):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    proxies = getProxy()
    while True:
        response = requests.head(url,headers={'cookie':cookie},proxies=proxies)
        print(response.headers)
        if response.headers.get('Location'):
            url = response.headers['Location']
        else:
            break
    file_size = int(requests.head(url).headers["Content-Length"])
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {
        "Range": "bytes=%s-%s" % (first_byte, file_size),
        'Cookie' : cookie,
        }
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=url.split('/')[-1])
    req = requests.get(url, headers=header, stream=True,proxies=proxies)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                pbar.update(chunk_size)
    pbar.close()
    return file_size

def aria2c(url,dst,cookie):
    os.system(f'aria2c "{url}" -o "{dst}" --header="Cookie: {cookie}"')

def getProxy():
    data = json.loads(open('proxy.json').read())
    sv = random.randrange(0,len(data)-1)
    proxy = data[sv]
    proxies = {
        'http': 'http://{}@{}:{}'.format(proxy['auth'],proxy['ip'],proxy['port']),
        'https' : 'http://{}@{}:{}'.format(proxy['auth'],proxy['ip'],proxy['port'])
    }   
    return proxies