#!/usr/bin/env python3
# coding=utf-8
# author: Qiu Huachuan
# Date: 2020-10-23

import os
from tkinter.filedialog import askdirectory
import csv
import json
import re


def main():
    path = askdirectory()
    all_file = os.listdir(path)
    all_text_files = []  # 存储文件名
    label_counter = {}  # 存储处理后的标签分类统计信息
    all_data = {}  # 存储读取所有标注文件的内容

    # 文件过滤
    for item in all_file:
        if item.endswith('.txt'):
            all_text_files.append(item)

    # 文件读取并临时汇总
    for item in all_text_files:
        with open(path + '/' + item, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            data = [line for line in reader]
            for el in data:
                if len(el) != 0:
                    index = re.findall('\d*', el[0])[0]
                    if index in all_data:
                        all_data[index].append(el[1])
                    else:
                        all_data[index] = [el[1]]

    # 标签统计
    for key in all_data:
        same_index_data = all_data[key]
        label_counter[key] = {}
        for el in same_index_data:
            el_list = el.split()
            if el_list[0] in label_counter[key]:
                label_counter[key][el_list[0]] += 1
            else:
                label_counter[key][el_list[0]] = 1

    # 将统计的数据存为json文件
    with open(path + '/label.json', 'w') as f:
        json.dump(label_counter, f)


if __name__ == "__main__":
    main()
