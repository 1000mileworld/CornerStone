import requests
import time
import pickle

def make_url(base_url,comp):
    url = base_url
    for r in comp:
        url = '{}/{}'.format(url,r)

    return url

def get_url(url,*args):
    content = requests.get(url)
    count = 1
    while content.status_code!=200: # keep trying until server says ok
        count+=1
        time.sleep(5)
        content = requests.get(url)
    if count>1:
        print(f'Success after {count} tries!')
    
    if len(args)>0:
        if args[0]=='content':
            return content.content
    return content.json()

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)