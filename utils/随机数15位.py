"""
    作者：徐富华
    日期：2019/9/5 19:51
    工具：PyCharm
    Python版本：3.7.0
"""
def random_order():
    import random
    import time
    # 随机七位数
    rd_seven = random.random()*10**7
    rd_seven = str(int(rd_seven))
    print(rd_seven)
    # 获取当前时间戳
    time_now = time.time()
    time_now = str(int(time_now))
    print(time_now)
    result = rd_seven+time_now
    return result
#字典转化为元组
def dic_lst_tp(dict1):
    list1 = []
    for i in dict1.values():
        list1.append(i)

    return list1

if __name__ == '__main__':
    dict1 ={"order_id":"2121","user_id":118}
    print(dic_lst_tp(dict1))

    # print(random_order())