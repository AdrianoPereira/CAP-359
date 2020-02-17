import numpy as np
import pandas as pd
import json
from datetime import datetime as dt
from download_data import download_glm, download_abi
from download_data import create_dataframe_glm, create_dataframe_abi


days = [338, 339]
hours = np.arange(0, 24)
minutes = np.arange(50, 60)


for day in days:
    times = dict()
    times[day] = {}
    for hour in hours:
        hour = str(hour).zfill(2)
        times[day][hour] = []
        for minute in minutes:
            minute = str(minute).zfill(2)
            times[day][hour].append(minute)

    with open('temp.json', 'w') as fp:
        json.dump(times, fp)


    data = dict()
    with open('temp.json') as json_file:
        data = json.load(json_file)

    for day in data.keys():
        for hour in data[day].keys():
            print('date', hour)
            date = dt.strptime('19%s' % day, '%y%j').date()
            date_time_str = '2019-%s-%s %s:%s:0' % (
                str(date.month).zfill(2), str(date.day).zfill(2),
                str(hour).zfill(2), str(data[day][hour][0]).zfill(2)
            )
            timestamp = dt.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            timestamp = dt.timestamp(timestamp)
            time = {
                'd': day,
                'h': hour,
                'm': data[day][hour],
                'y': 2019,
                't': int(timestamp)
            }
            path_glm = download_glm(time)
            path_abi = download_abi(time)
            create_dataframe_glm(path_glm, time)
            create_dataframe_abi(path_abi, time)

print(times)
