import sys
import csv
import os
from io import StringIO
from tqdm import tqdm
import math

def stat_origin_server(path = '../cdn_data/'):
    labels = ['time_stamp','host_id','object_id','size','start','end']
    files = os.listdir(path)
    server_count = {}
    obj_count = {}
    count = 0
    for cur_file in tqdm(files):
        if cur_file.endswith(".csv"):
            with open(path+cur_file,'r') as f:
                str_f = StringIO(f.read())
                csv_reader = csv.DictReader(str_f,fieldnames=labels)
                for i in csv_reader:
                    if int(i['end'])-int(i['start'])+1==int(i['size']) :
                        count += 1
                    # if i['host_id'] in server_count:
                    #     server_count[i['host_id']] += 1
                    # else :
                    #     server_count[i['host_id']] = 1
                    # if i['object_id'] in obj_count:
                    #     obj_count[i['object_id']] += 1
                    # else:
                    #     obj_count[i['object_id']] = 1

    print(count)
    # with open('./result.txt','w') as f:
    #     f.write(obj_count.__str__())
    # print("server info")
    # print(server_count)
    #
    # print("object info")
    # print('object number : ',len(obj_count))

    # print(obj_count)

def analyse(path='../cdn_data/',file_num=40):
    labels = ['time_stamp', 'host_id', 'object_id', 'size', 'start', 'end']
    files = os.listdir(path)
    files = files[0:file_num]
    time_series = {}

    for cur_file in tqdm(files):
        if cur_file.endswith(".csv"):
            with open(path + cur_file, 'r') as f:
                str_f = StringIO(f.read())
                csv_reader = csv.DictReader(str_f, fieldnames=labels)
                for i in csv_reader:
                    if not i['host_id'] in time_series:
                        time_series[i['host_id']] = {}
                    if not i['time_stamp'] in  time_series[i['host_id']]:
                        time_series[i['host_id']][i['time_stamp']] = 0
                    time_series[i['host_id']][i['time_stamp']] += 1
    return time_series

def group(data_list,group_size=10):
    count = 0
    _len = len(data_list)
    group_list = [0 for i in range(math.ceil(_len/group_size))]
    for i in data_list:
        group_list[int(count/group_size)] += data_list[i]
        count += 1
    return group_list

if __name__ == "__main__":
    stat_origin_server()