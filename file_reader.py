#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021/5/26 11:25 上午
# @Author  : Harvey Mei <harvey.mei@msn.com>
# @FileName: file_reader.py
# @IDE     : PyCharm
# @GitHub  : https://github.com/harveymei/
import json
import datetime
from matplotlib import pyplot as plt


filename = 'data.json'
date_list = []
usd_b_list, usd_s_list, eur_b_list, eur_s_list, hkd_b_list, hkd_s_list = [], [], [], [], [], []

with open(filename) as f_object:
    full_data = json.load(f_object)

    for data in full_data:
        date_list.append(datetime.datetime.strptime(data['date'], "%Y-%m-%d"))  # 日期字符串转日期对象写入列表
        usd_b_list.append(data['usd_cny']['buy_rate'])
        usd_s_list.append(data['usd_cny']['sell_rate'])
        eur_b_list.append(data['eur_cny']['buy_rate'])
        eur_s_list.append(data['eur_cny']['sell_rate'])
        hkd_b_list.append(data['hkd_cny']['buy_rate'])
        hkd_s_list.append(data['hkd_cny']['sell_rate'])

    print(date_list, usd_b_list)

# 两个或多个共享一个轴的图（解决多个y值差距较大，单图因比例问题影响细节显示）
# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/share_axis_lims_views.html
# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/shared_axis_demo.html
# 三位整数（行，列，索引），可逗号分隔或整体传入参数
fig = plt.figure(figsize=(10, 6), dpi=128)
fig.suptitle("Ping An Bank Forex Rate Per Day")
ax1 = plt.subplot(311)
ax1.plot(date_list, usd_b_list, c='red')
ax1.plot(date_list, usd_s_list, c='green')
ax1.set_ylabel("USD/CNY")
ax1.fill_between(date_list, usd_b_list, usd_s_list, facecolor='blue', alpha=0.1)  # 填充颜色
ax1.grid(True)  # 绘制网格

ax2 = plt.subplot(312, sharex=ax1)
ax2.plot(date_list, eur_b_list, c='red')
ax2.plot(date_list, eur_s_list, c='green')
ax2.set_ylabel("EUR/CNY")

ax3 = plt.subplot(313, sharex=ax1)
ax3.plot(date_list, hkd_b_list, c='red')
ax3.plot(date_list, hkd_s_list, c='green')
ax3.set_ylabel("HKD/CNY")  # 添加子图y轴标签

plt.show()
