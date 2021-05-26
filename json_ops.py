#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021/5/25 2:30 下午
# @Author  : Harvey Mei <harvey.mei@msn.com>
# @FileName: json_ops.py
# @IDE     : PyCharm
# @GitHub  : https://github.com/harveymei/

import json
import datetime

current_date = datetime.datetime.now().strftime("%Y-%m-%d")
print(current_date)
# 读取数据文件，不存在则创建，已读取内容作为字典，等待追加键值对
# data2 = {'abdc': 123, 'bcdd': 456}
with open('data.json', 'r') as f:
    data2 = json.load(f)

while True:
    key = input("输入键")
    if key == '':
        print("正在保存已录入数据")
        break

    value = input("输入值")
    if value == '':
        print("正在保存已录入数据")
        break

    data2[key] = value
    print("......")

# data2['defg'] = 234903
# data2['ghij'] = 9989

with open('data.json', 'wt', encoding='utf-8') as f_object:
    json.dump(data2, f_object)

print("已保存")
