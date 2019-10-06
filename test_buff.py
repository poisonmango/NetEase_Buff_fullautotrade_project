from IGXE_test import *
import re
import time

def search_target_lowestprice(game,good_id):
    b = buff_filter()
    r = b.search_goods_lowestprice(game,good_id)
    print(r)



def loading_target_goods():
    f = open("target_goods.txt","r")
    target_goods = []
    try:
        for i in f.readlines():
            result = re.match("([0-9]+).*?([0-9.]+)\n",i)
            good = []
            good.append(result.group(1))
            good.append(result.group(2))
            target_goods.append(good)
        f.close()
        return target_goods
    except:
        print(target_goods)
        print("发生导入错误!")
        f.close()
        return target_goods

def search_targets(game,target_goods):
    while True:
        b  = buff_filter()
        for i in target_goods:
            r = b.search_goods_lowestprice(game,i[0])
            print(r)
            if r!=0:
                if r < float(i[1]):
                    return i[0]
            else:
                print("某个结果出现0！")
                continue
        print("----一次循环结束----")
        time.sleep(3)

def search_target_lowest_price(game,good_id):
    b = buff_filter()
    r  = b.search_goods_lowestprice(game,good_id)
    return r



def make_order(game,good_id,price):
    return loginBuff.login_and_make_order(game,good_id,price)



if __name__ == '__main__':
    while True:
        try:
            # search_target_lowestprice("dota2","12195")
            # time.sleep(3)
            target_goods = loading_target_goods()
            # print(target_goods)
            target = search_targets("dota2",target_goods)
            price = search_target_lowest_price("dota2",target)
            r = make_order("dota2",target,price)
            if r == 0:
                print("购买成功！")
            elif r == 1:
                print("发生错误！")
            elif r == 2:
                print("价格错误！")
        except:
            continue


            #12.42 校园网
            #1999  沉寂  79