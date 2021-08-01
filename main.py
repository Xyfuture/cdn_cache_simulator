import sys
import csv
import os
from io import StringIO
from tqdm import tqdm
from replacement_algorithm import lru,base,content_aware



def evaluate(path='./cdn_data/'):
    # cdn_cache = lru.lru(50000000000)
    cdn_cache = content_aware.ContentAware(50000000000,'./config/cache_config.ini')
    labels = ['time_stamp', 'host_id', 'object_id', 'size', 'start', 'end']
    files = os.listdir(path)
    files = files[0:100]
    for cur_file in tqdm(files):
        if cur_file.endswith(".csv"):
            with open(path + cur_file, 'r') as f:
                str_f = StringIO(f.read())
                csv_reader = csv.DictReader(str_f, fieldnames=labels)
                for i in csv_reader:
                    req = base.SimpleRequest(i['object_id'],int(i['time_stamp']),int(i['size']),i['host_id'],int(i['start']),int(i['end']))
                    if not req.checkInterval(): # check start and end range
                        continue
                    # try:
                    if not cdn_cache.lookup(req): # check in cdn or not
                        cdn_cache.admit(req) # pull from remote
                    # except:
                    #     print(req.time,req.id)
    cdn_cache.statics()

if __name__ == "__main__":
    evaluate()
