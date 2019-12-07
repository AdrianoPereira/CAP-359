import subprocess
import os 
import numpy as np
import requests
from bs4 import BeautifulSoup
import datetime as dt


def request_l(query):
    out = subprocess.Popen([query], shell=True, stdout=subprocess.PIPE)
    l = out.communicate()[0].decode("utf-8") 
    buckets = l.replace('PRE', '').split()
    buckets = list(filter(lambda s: s.endswith('/'), buckets))
    
    return buckets


def request_f(query):
    out = subprocess.Popen([query], shell=True, stdout=subprocess.PIPE)
    l = out.communicate()[0].decode("utf-8") 
    buckets = l.split()
    buckets = list(filter(lambda s: len(s)>10, buckets))
    
    return buckets

def request_d(query):
    out = subprocess.Popen([query], shell=True, stdout=subprocess.PIPE)
    _ = out.communicate()[0].decode('utf-8') 
    
    print(_)

#list sensors
QUERY = 'aws s3 ls noaa-goes16'
#sensors = request_l(QUERY)
#print('sensors %s == %s'%(QUERY, sensors))

years = [2019]
days = np.arange(296, 299)+1
hours = list(map(lambda x: '%s'%str(x).zfill(2), np.arange(0, 24)))
sensors = ['ABI-L2-CMIPF']

for sensor in sensors:
    for year in years:
        for day in days:
            for hour in hours:
                PATH = '%s/%s/%s/%s/%s/'%(QUERY, sensor, year, day, hour)
                files = request_f(PATH)
                for file in files:
                    PATH = PATH.split()[-1]
#                    try:
#                        r = requests.get('http://www.dontpad.com/noaa-goes16')
#                        text = BeautifulSoup(r.text, 'html.parser')
#                        text = text.textarea.text
#                        d = dt.datetime.now()
#                        d = '%s/%s/%s, %s:%s:%s'%(d.day, d.month, d.year, 
#                                                  d.hour, d.minute, d.second)
#                        text += '\n%s\n'%d
#                        payload = {
#                            'text': text+'%s/%s'%(PATH, file)
#                        }
#                        r = requests.post('http://www.dontpad.com/noaa-goes16', 
#                                          data=payload)
#                    except:
#                        print('Error dontpad')

                    if not os.path.exists(PATH):
                        os.makedirs(PATH)
                    print('Saving %s in %s ', file, PATH)
                    q = 'aws s3 cp s3://%s%s %s'%(PATH, file, PATH)
                    request_d(q)
                    
print('finished...')












