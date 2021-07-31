import sys
import csv
import os
from io import StringIO
from tqdm import tqdm


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


if __name__ == "__main__":
    stat_origin_server()