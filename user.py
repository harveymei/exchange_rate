#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021/5/25 12:12 下午
# @Author  : Harvey Mei <harvey.mei@msn.com>
# @FileName: user.py
# @IDE     : PyCharm
# @GitHub  : https://github.com/harveymei/

import json

filename = 'data.json'
with open(filename) as f_object:
    full_data = json.load(f_object)  # 使用Json解码可正常识别[]为空列表，而不是字符串

    while True:
        input_key_1 = "date"
        input_value_1 = input("请输入日期：（YYYY-MM-DD）")
        if input_value_1 == '':
            break

        input_key_2 = "usd_cny"
        buy_rate_2 = float(input("请输入USD买入价："))
        sell_rate_2 = float(input("请输入USD卖出价："))
        input_value_2 = {"buy_rate": buy_rate_2, "sell_rate": sell_rate_2}

        input_key_3 = "eur_cny"
        buy_rate_3 = float(input("请输入EUR买入价："))
        sell_rate_3 = float(input("请输入EUR卖出价："))
        input_value_3 = {"buy_rate": buy_rate_3, "sell_rate": sell_rate_3}

        input_key_4 = "hkd_cny"
        buy_rate_4 = float(input("请输入HKD买入价："))
        sell_rate_4 = float(input("请输入HKD卖出价："))
        input_value_4 = {"buy_rate": buy_rate_4, "sell_rate": sell_rate_4}

        rate_record = {
            input_key_1: input_value_1,
            input_key_2: input_value_2,
            input_key_3: input_value_3,
            input_key_4: input_value_4
        }

        full_data.append(rate_record)

print(full_data)
with open(filename, 'wt') as f_object:
    json.dump(full_data, f_object, indent=4)  # 缩进格式
