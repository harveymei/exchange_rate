#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2021/5/25 12:12 下午
# @Author  : Harvey Mei <harvey.mei@msn.com>
# @FileName: forex_rate.py
# @IDE     : PyCharm
# @GitHub  : https://github.com/harveymei/

"""
分析每工作日美元/欧元/港币与人民币的买入卖出汇率
数据来源：平安银行每工作日10点钟汇率订阅短信息
round()函数截取小数点后n位且不会四舍五入
缩进格式写入json数据（易于阅读）

需求：使用subplot绘制多图
绘制多图解决不同货币汇率差异较大导致的显示比例问题

新增英镑数据后，兼容历史数据的处理和0值数据影响图形比例问题的处理：
1，在读取数据文件阶段，针对异常进行补0值操作
2，在图形生成阶段，不绘制历史时间轴上的0值数据

新需求：选择按月（1-n个月）或年（1-n个年）生成图表
指定起始和终止的月份/年份
新需求：选择货币（1-4）

"""

import json
from datetime import datetime as dt  # 减少输入
from matplotlib import pyplot as plt
from matplotlib import font_manager as mfm  # 加入中文字体支持


def rate_input():
    """
    定义汇率录入函数
    """
    filename = 'data.json'
    with open(filename, 'r') as f_object:
        full_data = json.load(f_object)  # 使用Json解码可正常识别[]为空列表，而不是字符串

    while True:
        input_key_1 = "date"
        input_value_1 = input("请输入日期（YYYY-MM-DD）\n"
                              "或直接按回车键退出录入并返回主菜单：")
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

        input_key_5 = "gbp_cny"
        buy_rate_5 = float(input("请输入GBP买入价："))
        sell_rate_5 = float(input("请输入GBP卖出价："))
        input_value_5 = {"buy_rate": buy_rate_5, "sell_rate": sell_rate_5}

        # 拼接字典键值赋值变量
        rate_record = {
            input_key_1: input_value_1,
            input_key_2: input_value_2,
            input_key_3: input_value_3,
            input_key_4: input_value_4,
            input_key_5: input_value_5
        }

        # 将字典作为列表元素追加写入列表
        full_data.append(rate_record)

        # 于每次录入四组汇率后将更新后的列表写入文件
        with open(filename, 'w') as f:  # 不指定操作模式时，报io.UnsupportedOperation: not writable异常
            json.dump(full_data, f, indent=4)  # 缩进格式


def rate_output():
    """
    定义汇率分析函数
    """
    filename = 'data.json'
    date_list = []
    usd_b_list, usd_s_list = [], []
    eur_b_list, eur_s_list = [], []
    hkd_b_list, hkd_s_list = [], []
    gbp_b_list, gbp_s_list = [], []

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
            # 添加异常处理，处理数据文件早期无英镑汇率的数据读取问题
            try:
                gbp_b_list.append(data['gbp_cny']['buy_rate'])
            except KeyError:  # 读取数据产生KeyError异常（不存在）时捕获异常并在列表追加写入0值（坐标y值）
                gbp_b_list.append(0)
            try:
                gbp_s_list.append(data['gbp_cny']['sell_rate'])
            except KeyError:
                gbp_s_list.append(0)

        # print(date_list, usd_b_list)

    zero_count = gbp_b_list.count(0)  # 固定值，计算英镑买入价列表中0值的数量（早期历史数据中不含英镑价格的数量）

    # 指定中文字体
    font_path = 'SourceHanSerifSC-Light.otf'  # 思远宋体Light（简体中文）
    prop = mfm.FontProperties(fname=font_path)

    # 两个或多个共享一个轴的图（解决不同y值差距较大，单图因比例问题影响细节显示）
    # Subplots Layout 多图布局
    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/share_axis_lims_views.html
    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/shared_axis_demo.html
    # 三位整数（行，列，索引），可逗号分隔或整体传入参数
    fig = plt.figure(figsize=(10, 8), dpi=128)  # 设置图表尺寸及解析度（点数每英寸，1英寸=2.54厘米）
    # 新增英镑汇率后，图表尺寸由10:6调整为10:8比例
    fig.suptitle("平安银行每工作日汇率分析\n（美元/欧元/港币/英镑）", fontsize=24, fontproperties=prop)  # 设置多图标题

    ax1 = plt.subplot(411)  # 绘图（4行，1列，第1幅）
    ax1.plot(date_list, usd_b_list, c='red')
    ax1.plot(date_list, usd_s_list, c='blue')
    # ax1.fill_between(date_list, usd_b_list, usd_s_list, facecolor='blue', alpha=0.1)  # 填充颜色
    ax1.set_ylabel("USD/CNY", fontsize=16)
    ax1.grid(True)  # 绘制网格
    # https://matplotlib.org/stable/api/legend_api.html
    # 图例位置参数loc默认为最佳位置（自动）
    ax1.legend(('buy_rate', 'sell_rate'), fontsize=8, loc='lower left')  # 添加图例，指定字体大小及位置（左下方）

    ax2 = plt.subplot(412, sharex=ax1)  # 绘图（4行，1列，第2幅）,共享第一幅x轴
    # 颜色设置
    # https://matplotlib.org/stable/tutorials/colors/colors.html
    # https://matplotlib.org/stable/gallery/color/named_colors.html （颜色名称列表）
    ax2.plot(date_list, eur_b_list, color='green')  # 绿色
    ax2.plot(date_list, eur_s_list, color='pink')  # 粉红色
    ax2.set_ylabel("EUR/CNY", fontsize=16)
    ax2.grid(True)
    ax2.legend(('buy_rate', 'sell_rate'), fontsize=8, loc='lower left')

    ax3 = plt.subplot(413, sharex=ax1)  # 绘图（4行，1列，第3幅）,共享第一幅x轴
    ax3.plot(date_list, hkd_b_list, c='m')  # magenta 洋红色
    ax3.plot(date_list, hkd_s_list, c='k')  # black 黑色
    ax3.set_ylabel("HKD/CNY", fontsize=16)  # 添加子图y轴标签
    # ax3.set_xlabel("Weekday", fontsize=16)  # 仅在第三幅图显示x轴标签
    ax3.grid(True)
    ax3.legend(('buy_rate', 'sell_rate'), fontsize=8, loc='lower left')
    # fig.autofmt_xdate()  # 仅在第3幅图处绘制斜的x轴日期标签，默认参数值为右对齐旋转30度

    # 新增英镑汇率 2021-06-16
    ax4 = plt.subplot(414, sharex=ax1)
    # 取原始列表中非0值元素作为x坐标值列表和y坐标值列表，传入参数
    # 不绘制历史时间段中y值为0值（实际缺失）的部分，避免影响显示比例
    ax4.plot(date_list[zero_count:], gbp_b_list[zero_count:], c='brown')  # 棕色
    ax4.plot(date_list[zero_count:], gbp_s_list[zero_count:], c='cyan')  # 青色
    ax4.set_ylabel("GBP/CNY", fontsize=16)
    ax4.set_xlabel("Weekday", fontsize=16)  # 调整为仅在第四幅图显示x轴坐标
    ax4.grid(True)
    ax4.legend(("buy_rate", 'sell_rate'), fontsize=8, loc='lower left')
    fig.autofmt_xdate()  # 调整为仅在第4幅图处绘制斜的x轴日期标签，默认参数值为右对齐旋转30度

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
