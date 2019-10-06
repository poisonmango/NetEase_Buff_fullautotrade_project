import  requests
import re
import os
import threading
import sys
import datetime
import numpy as np
import time
import loginBuff

class buff_filter():
    def __init__(self):
        self.header = {
            'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        self.session = requests.Session()
        # self.cookie = "mail_psc_fingerprint=0694a4235e7ae6cc1cb7372df5891c5e; usertrack=CrHueVvMNI+MVyCQA60NAg==; _ntes_nnid=e6ed0a3ed4c780ccd1ee2f470fabd5ed,1540109340046; _ntes_nuid=e6ed0a3ed4c780ccd1ee2f470fabd5ed; vjuids=-1f29af9a6.1669bd949ed.0.de0e04fb2e0c8; vjlast=1540213001.1540213001.30; __gads=ID=eacb92166e9c6e53:T=1540213124:S=ALNI_MZu7sfdfQcTfmqOErAev_A3Vn-doQ; _ga=GA1.2.227678621.1540304274; Hm_lvt_f946fdf4484c5178b3e5ea1a72d4a75c=1543326680,1544014297,1544147602,1544588392; vinfo_n_f_l_n3=79a1fdc0c0b4e043.1.2.1540213000735.1551491964883.1553941945263; Province=010; City=010; csrf_token=80f4d495b18627336598899c564545e307f2e28c; game=dota2; _gid=GA1.2.1836620841.1557887127; NTES_YD_SESS=a5zktUZHfSLZPiLgCh_U.qJGiK9aOkaKSu2XB6nWBwCoKp8LKuA4P3ofhxWYafwKt_oj9V.sIHDv0OimNm8jwKlZ5i2mF5Fg6i566JXUx4fOwuj.rwzEA5Bh7yL2BBq9ofoaahnnZyWA3aXtujs.gNXHQPGxD8CXeAC46RQJsRYA.5P03TGyFat4f__yEr3RU0C_tBjm6PTx8WotppFjLhGAEC6Se10LhCPTVqm75dyDg; S_INFO=1557887237|0|3&80##|17600870550; P_INFO=17600870550|1557887237|1|netease_buff|00&99|bej&1557879907&netease_buff#bej&null#10#0#0|&0|null|17600870550; session=1-mWokS7O3yIP1h-pwVs3tHXObSsT1UOEIW7ik8oxR5X_A2046056609; _gat_gtag_UA_109989484_1=1"
        # self.cookies = dict(map(lambda x:x.split('='),self.cookie.split(";")))
        # for k,v in self.cookies.items():
        #     self.session.cookies.set(k,v)
        self.session.headers.update({
            'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            'Cookie':"mail_psc_fingerprint=0694a4235e7ae6cc1cb7372df5891c5e; usertrack=CrHueVvMNI+MVyCQA60NAg==; _ntes_nnid=e6ed0a3ed4c780ccd1ee2f470fabd5ed,1540109340046; _ntes_nuid=e6ed0a3ed4c780ccd1ee2f470fabd5ed; vjuids=-1f29af9a6.1669bd949ed.0.de0e04fb2e0c8; vjlast=1540213001.1540213001.30; __gads=ID=eacb92166e9c6e53:T=1540213124:S=ALNI_MZu7sfdfQcTfmqOErAev_A3Vn-doQ; _ga=GA1.2.227678621.1540304274; Hm_lvt_f946fdf4484c5178b3e5ea1a72d4a75c=1543326680,1544014297,1544147602,1544588392; vinfo_n_f_l_n3=79a1fdc0c0b4e043.1.2.1540213000735.1551491964883.1553941945263; Province=010; City=010; csrf_token=80f4d495b18627336598899c564545e307f2e28c; game=dota2; _gid=GA1.2.1836620841.1557887127; NTES_YD_SESS=a5zktUZHfSLZPiLgCh_U.qJGiK9aOkaKSu2XB6nWBwCoKp8LKuA4P3ofhxWYafwKt_oj9V.sIHDv0OimNm8jwKlZ5i2mF5Fg6i566JXUx4fOwuj.rwzEA5Bh7yL2BBq9ofoaahnnZyWA3aXtujs.gNXHQPGxD8CXeAC46RQJsRYA.5P03TGyFat4f__yEr3RU0C_tBjm6PTx8WotppFjLhGAEC6Se10LhCPTVqm75dyDg; S_INFO=1557887237|0|3&80##|17600870550; P_INFO=17600870550|1557887237|1|netease_buff|00&99|bej&1557879907&netease_buff#bej&null#10#0#0|&0|null|17600870550; session=1-mWokS7O3yIP1h-pwVs3tHXObSsT1UOEIW7ik8oxR5X_A2046056609; _gat_gtag_UA_109989484_1=1"
        })

    def login(self):
        pass


    def search_goods_lowestprice(self,game,good_id):
        try:
            url = "https://buff.163.com/api/market/goods/sell_order?game="+game+"&goods_id="+good_id
            r = self.session.get(url)
            if r.status_code==200:
                find_price =  re.search('"price": "(.*?)"',r.content.decode('utf-8'))
                return float(find_price.group(1))
            else:
                print("状态码不是200")
                return 0
        except:
            return 0

    def search_goods_avgprice_by_orders(self,game,good_id):
        url = "https://buff.163.com/api/market/goods/bill_order?game="+game+"&goods_id="+good_id
        r = self.session.get(url)
        try:
            if r.status_code==200:
                find_allprice = re.findall('"price": "(.*?)"',r.content.decode('utf-8'))
                find_allprice = [ float(i) for i in find_allprice]
                allprice = 0
                if len(find_allprice)>7:
                    for i in range(3):
                        allprice += find_allprice[i]
                    avg = allprice/3
                    # allprice=0
                    # for i in range(3):
                    #     allprice += min(find_allprice)
                    #     find_allprice.remove(min(find_allprice))
                    # avg2 = allprice/3
                    # avg = avg1*0.3 + 0.7*avg2
                    return avg
                else:
                    return 0
            else:
                print("状态码不是200")
                return 0
        except:
            return 0

    def search_goods_avgprice_by_grid(self,game,good_id):
        url = "https://buff.163.com/api/market/goods/price_history/buff?game=" + game + "&goods_id=" + good_id + "&currency=CNY"
        r = self.session.get(url)
        find_history = re.search('"price_history": \[(.*)\],', r.text, re.S).group(1)
        find_all_history = re.findall('([0-9.]+),.*?([0-9.]+).*?]', find_history, re.S)
        all_history_price = []
        for i in find_all_history:
            all_history_price.append(i[1])
        # print(all_history_price)
        # print(len(all_history_price))
        all_history_price.reverse()
        mount = int(len(all_history_price)/3)
        all_price = 0
        latest_price = []
        for i in range(mount):
            all_price+= float(all_history_price[i])
            latest_price.append(float(all_history_price[i]))
        avg_price = all_price/mount
        lowest_price = min(latest_price)
        highest_price = max(latest_price)
        target_price = (highest_price+avg_price)/2
        ischeap_price = (avg_price+lowest_price)/2
        return target_price,ischeap_price

    def judge_is_cheap(self,game,good_id):
        try:
            lowestprice = self.search_goods_lowestprice(game,good_id)
            avglow,avghigh = self.search_goods_avgprice_by_grid(game,good_id)
            print(lowestprice,avglow)
            if lowestprice<2 or avglow ==0 :
                return 0,0
            elif lowestprice < 100  and ((avghigh-avglow)/avglow>0.05 or avghigh-avglow>5 ) and lowestprice<avglow/0.99:
                return good_id,lowestprice
            else:
                return 0,0
        except:
            return 0,0

    def search_all_hot_goods(self,game,stard_id,end_id):
        start = stard_id
        hotlist = []
        for i in range(end_id-stard_id):
            r = self.judge_is_hot_by_pricehistory(game,str(start))    #判断是否热销
            if r!=0:
                p = self.search_goods_lowestprice(game,str(start))
                if p > 15 :                                           #低于15元的不要
                    hotlist.append(r)
                    print("id:" + str(start) + r)
                    start+=1
                else:
                    print("id:" + str(start) + " 0")
                    start += 1
                    continue
            else:
                print("id:" + str(start) + " 0" )
                start+=1
                continue
        return hotlist

    def judge_is_hot(self,game,good_id):   #基于订单列表(最多10个)今天的订单数量来判断
        url = "https://buff.163.com/api/market/goods/bill_order?game=" + game + "&goods_id=" + good_id
        r = self.session.get(url)
        find_all_buydate_origin = re.findall('"transact_time": (.*?),',r.content.decode('utf-8'))
        find_all_buydate_origin = [datetime.datetime.fromtimestamp(int(i)) for i in find_all_buydate_origin]
        # print(len(find_all_buydate_origin))
        gap=[]
        if len(find_all_buydate_origin)>7:
            for i in range(5):
                s = re.match("(.*?) day",str(datetime.datetime.now()-find_all_buydate_origin[i]))
                if s == None:
                    gap.append('0')
                else:
                    gap.append(s.group(1))
            gap = [int(i) for i in gap]
            # print(gap)
            if max(gap)>3:
                return 0
            else:
                return good_id
        else:
            return 0


    def judge_is_hot_by_pricehistory(self,game,good_id):    #基于7日内销售图表是否大于120
        url =  "https://buff.163.com/api/market/goods/price_history/buff?game="+game+"&goods_id="+good_id+"&currency=CNY"
        try:
            r = self.session.get(url)
            find_history = re.search('"price_history": \[(.*)\],',r.text,re.S).group(1)
            find_all_history = re.findall('([0-9.]+),.*?([0-9.]+).*?]',find_history,re.S)
        except:
            return 0
        all_history_time = []
        all_history_price = []
        for i in find_all_history:
            all_history_time.append(datetime.datetime.fromtimestamp(int(i[0])/1000))
            all_history_price.append(i[1])
        # print(all_history_time)
        # print(all_history_price)
        # print(len(all_history_price))
        if len(all_history_price)>60:
            return good_id
        else:
            return 0

    def make_order(self,game,good_id):
        refresh_url = "https://buff.163.com/"
        refresh_r = self.session.get(refresh_url)
        url = "https://buff.163.com/api/market/goods/sell_order?game="+game+"&goods_id=" + good_id
        r = self.session.get(url)
        if r.status_code == 200:
            id = re.search('"id": "(.*?)",',r.text).group(1)
            price = re.search('"price": "(.*?)",',r.text).group(1)
            print(id,price)
            url_0 = "https://buff.163.com/api/message/notification?_="+str(int((float(datetime.datetime.timestamp(datetime.datetime.now()))*1000)))
            # print(str(int((float(datetime.datetime.timestamp(datetime.datetime.now()))*1000))))
            # print(str(int((float(datetime.datetime.timestamp(datetime.datetime.utcnow()))*1000))))
            url_0_r = self.session.get(url_0,headers = {"Referer":"https://buff.163.com/market/goods?goods_id="+good_id+"&from=market"})
            url_1 = "https://buff.163.com/account/api/user/info?_="+str(int((float(datetime.datetime.timestamp(datetime.datetime.now()))*1000)))
            url_1_r = self.session.get(url_1,headers = {"Referer":"https://buff.163.com/market/goods?goods_id="+good_id+"&from=market"})
            # print(url_1_r.status_code)
            # print(url_1_r.text)
            url_2 = "https://buff.163.com/api/market/goods/buy/preview?game="+game+"&sell_order_id="+id+"&goods_id="+good_id+"&price="+price+"&allow_tradable_cooldown=0&_="+str(int((float(datetime.datetime.timestamp(datetime.datetime.now()))*1000)))
            url_2_r = self.session.get(url_2,headers = {"Referer":"https://buff.163.com/market/goods?goods_id="+good_id+"&from=market"})
            print(url_2_r.cookies)
            # print(url_2_r.status_code)
            # print(url_2_r.text)
            buy_url = "https://buff.163.com/api/market/goods/buy"
            post_data = { "allow_tradable_cooldown":0,
                          "game":"dota2",
                          "goods_id":good_id,
                          "pay_method":3,
                          "price":float(price),
                          "sell_order_id":id,
                          "token":""
            }
            order = self.session.post(buy_url,data=post_data)
            if order.status_code == 200:
                print(order.text)
                return 1
            else:
                print(order.status_code)
                return 0
        else:
            return 0

def foreach(buff_filter,start_id,end_id):
    for i in range(start_id,end_id):
        print(i)
        result,lowestprice = buff_filter.judge_is_cheap('dota2',str(i))
        if result!=0:
            print("找到！------------------------------",result)
            f = open("result.txt", 'a')
            f.write(result+"  价格："+str(lowestprice)+"\n")
            f.flush()
            f.close()
            continue
        else:
            continue
        # else:
        #     result = buff_filter.judge_is_cheap("csgo",str(i))
        #     if result!=0:
        #         print("找到！-------------------------------", result)
        #         f = open("result.txt", 'a')
        #         f.write(result + "\n")
        #         f.flush()
        #         f.close()
        #         continue
        #     else:
        #         continue


def find_hot_goods(buff_filter,start_id,end_id):
        result = buff_filter.search_all_hot_goods('dota2',start_id,end_id)
        f = open("hotlist.txt", 'a')
        for i in result:
            f.write(i+'\n')
        f.flush()
        f.close()

if __name__ == '__main__':
    b = buff_filter()
    # s = b.search_goods_avgprice_by_grid("dota2","16489")   #759919   135
    # print(s)
    # game = "dota2"
    # good_id = "937"
    # print(b.search_goods_avgprice_by_grid(game,good_id))
    # print(b.search_goods_lowestprice(game,good_id))
    # while True:
    #     price = b.search_goods_lowestprice(game,good_id)
    #     print(price)
    #     if price<0.20:
    #         loginBuff.main(game,good_id)
    #         print("---购买完成！！！---")
    #         break
    #     else:
    #         print("价格太高！")

    # while True:
    try:
        for i in range(5):
            if i == 0:
                t = threading.Thread(target=find_hot_goods,args=(b,60000,64000))
                print("t1 start!")
                t.start()

            elif i == 1:
                t = threading.Thread(target=find_hot_goods, args=(b,64000,68000))
                print("t2 start!")
                t.start()
            elif i == 2:
                t = threading.Thread(target=find_hot_goods, args=(b,68000,72000))
                print("t3 start!")
                t.start()
            elif i == 3:
                t = threading.Thread(target=find_hot_goods, args=(b,72000,76000))
                print("t4 start!")
                t.start()
            else:
                t = threading.Thread(target=find_hot_goods, args=(b,76000,80000))
                print("t5 start!")
                t.start()
                t.join()
    except:
        print("error!")
        sys.exit(0)


# https://buff.163.com/api/market/goods/price_history/buff?game=dota2&goods_id=7684&currency=CNY&_=1540994660 901
#策略改为计算价格趋势图的均价，购买均价以下的商品，在高点卖出   需要改：1.avg方法 2.ischeap方法 3.foreach函数
# (148.867301625, 488.02500000000003, 239.36450000000002, 251.1503411438356)