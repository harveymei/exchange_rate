#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021/5/25 12:12 下午
# @Author  : Harvey Mei <harvey.mei@msn.com>
# @FileName: forex_rate.py
# @IDE     : PyCharm
# @GitHub  : https://github.com/harveymei/

"""
数据来源：平安银行每工作日10点钟汇率订阅短信息
round()函数截取小数点后n位且不会四舍五入
缩进格式写入json数据（易于阅读）
使用subplot绘制多图
"""

import json
from datetime import datetime as dt  # 减少输入
from matplotlib import pyplot as plt


def rate_input():
    """
    定义汇率录入函数
    """
    filename = 'data.json'
    with open(filename) as f_object:
        full_data = json.load(f_object)  # 使用Json解码可正常识别[]为空列表，而不是字符串

        while True:
            input_key_1 = "date"
            input_value_1 = input("请输入日期：（YYYY-MM-DD）\n"
                                  "或直接敲回车键退出录入返回主菜单 ")
            if input_value_1 == '':
                # break
                rate_menu()  # 退回主菜单

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

            # 拼接字典键值赋值变量
            rate_record = {
                input_key_1: input_value_1,
                input_key_2: input_value_2,
                input_key_3: input_value_3,
                input_key_4: input_value_4
            }

            # 将字典作为列表元素追加写入列表
            full_data.append(rate_record)

            # 于每次录入三组汇率后将更新后的列表写入文件
            json.dump(full_data, f_object, indent=4)  # 缩进格式


def rate_output():
    """
    定义汇率分析函数
    """
    filename = 'data.json'
    date_list = []
    usd_b_list, usd_s_list, eur_b_list, eur_s_list, hkd_b_list, hkd_s_list = [], [], [], [], [], []

    with open(filename) as f_object:
        full_data = json.load(f_object)

        # 遍历当前文件中字典键值放入列表
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
    fig = plt.figure(figsize=(10, 6), dpi=128)  # 设置图表尺寸及解析度（点数每英寸）
    fig.suptitle("Ping An Bank Forex Rate Per Weekday", fontsize=24)  # 设置多图标题

    ax1 = plt.subplot(311)  # 绘图（3行，1列，第1幅）
    ax1.plot(date_list, usd_b_list, c='red')
    ax1.plot(date_list, usd_s_list, c='blue')
    # ax1.fill_between(date_list, usd_b_list, usd_s_list, facecolor='blue', alpha=0.1)  # 填充颜色
    ax1.set_ylabel("USD/CNY", fontsize=16)
    ax1.grid(True)  # 绘制网格
    # https://matplotlib.org/stable/api/legend_api.html
    # 图例位置参数loc默认为最佳位置（自动）
    ax1.legend(('buy_rate', 'sell_rate'), fontsize=8, loc='lower left')  # 添加图例，指定字体大小及位置（左下方）

    ax2 = plt.subplot(312, sharex=ax1)  # 绘图（3行，1列，第2幅）,共享第一幅x轴
    # https://matplotlib.org/stable/tutorials/colors/colors.html
    ax2.plot(date_list, eur_b_list, color='green')
    ax2.plot(date_list, eur_s_list, color='pink')
    ax2.set_ylabel("EUR/CNY", fontsize=16)
    ax2.grid(True)
    ax2.legend(('buy_rate', 'sell_rate'), fontsize=8, loc='lower left')

    ax3 = plt.subplot(313, sharex=ax1)  # 绘图（3行，1列，第3幅）,共享第一幅x轴
    ax3.plot(date_list, hkd_b_list, c='m')  # magenta 洋红色
    ax3.plot(date_list, hkd_s_list, c='k')  # black 黑色
    ax3.set_ylabel("HKD/CNY", fontsize=16)  # 添加子图y轴标签
    ax3.set_xlabel("Weekday", fontsize=16)  # 仅在第三幅图显示x轴标签
    ax3.grid(True)
    ax3.legend(('buy_rate', 'sell_rate'), fontsize=8, loc='lower left')
    fig.autofmt_xdate()

    # plt.show()
    # 使用精确到秒的当前时间作为随机文件名
    plt.savefig(dt.now().strftime("%Y%m%d%H%M%S") + ".png")

    print("数据分析完成，返回主菜单")
    rate_menu()


def rate_menu():
    """
    定义主菜单函数
    """
    print("\n请选择将要执行的操作\n"
          "1) 录入数据\n"
          "2) 分析数据\n"
          "3) 退出程序\n"
          )

    option = input("请输入选项值并按回车键确认：")
    if option == '1':
        print("开始录入数据")
        rate_input()
    elif option == '2':
        print("开始分析数据")
        rate_output()
    elif option == '3':
        print("程序退出")
        exit()
    else:
        print("无效输入")
        rate_menu()


"""
执行程序
"""
rate_menu()
