#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021/5/25 12:12 下午
# @Author  : Harvey Mei <harvey.mei@msn.com>
# @FileName: user.py
# @IDE     : PyCharm
# @GitHub  : https://github.com/harveymei/

"""
数据来源：平安银行每工作日10点钟汇率订阅短信息
使用round()函数处理录入浮点数省略0的问题
缩进格式写入json数据（易于阅读）
"""
import json
from datetime import datetime as dt  # 减少输入
from matplotlib import pyplot as plt


def rate_input():
    filename = 'data.json'
    with open(filename) as f_object:
        full_data = json.load(f_object)  # 使用Json解码可正常识别[]为空列表，而不是字符串

        while True:
            input_key_1 = "date"
            input_value_1 = input("请输入日期：（YYYY-MM-DD）\n"
                                  "或直接敲回车键退出录入返回主菜单 ")
            if input_value_1 == '':
                # break
                menu.rate_menu()  # 退回主菜单

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

        with open(filename, 'wt') as f_object:
            json.dump(full_data, f_object, indent=4)  # 缩进格式


def data_outpu():
    filename = 'data.json'
    date_list = []
    usd_b_list, usd_s_list, eur_b_list, eur_s_list, hkd_b_list, hkd_s_list = [], [], [], [], [], []

    with open(filename) as f_object:
        full_data = json.load(f_object)

        for data in full_data:
            date_list.append(dt.strptime(data['date'], "%Y-%m-%d"))  # 日期字符串转日期对象写入列表
            usd_b_list.append(data['usd_cny']['buy_rate'])
            usd_s_list.append(data['usd_cny']['sell_rate'])
            eur_b_list.append(data['eur_cny']['buy_rate'])
            eur_s_list.append(data['eur_cny']['sell_rate'])
            hkd_b_list.append(data['hkd_cny']['buy_rate'])
            hkd_s_list.append(data['hkd_cny']['sell_rate'])

        # print(date_list, usd_b_list)

    # 两个或多个共享一个轴的图（解决不同y值差距较大，单图因比例问题影响细节显示）
    # Subplots Layout 多图布局
    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/share_axis_lims_views.html
    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/shared_axis_demo.html
    # 三位整数（行，列，索引），可逗号分隔或整体传入参数
    fig = plt.figure(figsize=(10, 6), dpi=128)
    fig.suptitle("Ping An Bank Forex Rate Per Weekday", fontsize=24)

    ax1 = plt.subplot(311)  # 绘图（3行，1列，第1幅）
    ax1.plot(date_list, usd_b_list, c='red')
    ax1.plot(date_list, usd_s_list, c='blue')
    # ax1.fill_between(date_list, usd_b_list, usd_s_list, facecolor='blue', alpha=0.1)  # 填充颜色
    ax1.set_ylabel("USD/CNY", fontsize=16)
    ax1.grid(True)  # 绘制网格

    ax2 = plt.subplot(312, sharex=ax1)  # 绘图（3行，1列，第2幅）,共享第一幅x轴
    ax2.plot(date_list, eur_b_list, c='red')
    ax2.plot(date_list, eur_s_list, c='blue')
    ax2.set_ylabel("EUR/CNY", fontsize=16)
    ax2.grid(True)

    ax3 = plt.subplot(313, sharex=ax1)  # 绘图（3行，1列，第3幅）,共享第一幅x轴
    ax3.plot(date_list, hkd_b_list, c='red')
    ax3.plot(date_list, hkd_s_list, c='blue')
    ax3.set_ylabel("HKD/CNY", fontsize=16)  # 添加子图y轴标签
    ax3.set_xlabel("Weekday", fontsize=16)  # 仅在第三幅图显示x轴标签
    ax3.grid(True)
    fig.autofmt_xdate()

    # plt.show()
    plt.savefig(dt.now().strftime("%Y%m%d%H%M%S") + ".png")


def rate_menu():
    print("请选择将要执行的操作\n"
          "1) 录入数据\n"
          "2) 分析数据\n"
          "3) 退出程序\n"
          )

    option = input("输入选项值并按回车键确认：")
    if option == '1':
        data_input.rate_input()
    elif option == '2':
        data_output.rate_output()
    elif option == '3':
        exit()
    else:
        print("无效输入")
        rate_menu()