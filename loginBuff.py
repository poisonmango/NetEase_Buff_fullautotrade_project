from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import requests
import cv2
import numpy as np
import time

def match(target, template):
    img_rgb = cv2.imread(target)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template, 0)
    run = 1
    w, h = template.shape[::-1]
    print(w, h)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    # 使用二分法查找阈值的精确值
    L = 0
    R = 1
    while run < 20:
        run += 1
        threshold = (R + L) / 2
        print(threshold)
        if threshold < 0:
            print('Error')
            return None
        loc = np.where(res >= threshold)
        print(len(loc[1]))
        if len(loc[1]) > 1:
            L += (R - L) / 2
        elif len(loc[1]) == 1:
            print('目标区域起点x坐标为：%d' % loc[1][0])
            break
        elif len(loc[1]) < 1:
            R -= (R - L) / 2

    return loc[1][0]

def get_tracks(distance):
    print(distance)
    distance += 20
    v = 0
    t = 0.2
    forward_tracks = []
    current = 0
    mid1 = distance * 1 / 3
    mid2 = distance * 2 / 3
    while current < distance:
        if current < mid1:
            a = 2
        elif current < mid2:
            a = 1
        else:
            a = -2
        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        forward_tracks.append(round(s))

    back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
    return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}

def drag_block(dr):
    code = dr.find_element_by_class_name("yidun_bg-img")
    block = dr.find_element_by_class_name("yidun_jigsaw")
    code_src = code.get_property("src")
    block_src = block.get_property("src")
    # print(code_src)
    # print(block_src)

    time.sleep(1)
    yanzheng = requests.get(code_src)
    f = open("code_image.jpg", "wb")
    f.write(yanzheng.content)
    f.close()

    blockimg = requests.get(block_src)
    f = open("block_image.png", "wb")
    f.write(blockimg.content)
    f.close()

    all = 0
    distance = match("code_image.jpg", "block_image.png")
    if distance > 120:
        slider = dr.find_element_by_class_name("yidun_slider__icon")
        ac = ActionChains(dr)
        ac.move_to_element(slider).perform()
        time.sleep(2)
        refresh = dr.find_element_by_class_name("yidun_refresh")
        refresh.click()
        time.sleep(1)
        drag_block(dr)
        return True
    else:
        tracks = get_tracks(distance)
        print(tracks)
        slider = dr.find_element_by_class_name("yidun_slider__icon")
        ac = ActionChains(dr)
        ac.click_and_hold(slider).perform()
        for track in tracks['forward_tracks']:
            ac.move_by_offset(xoffset=track, yoffset=0).perform()
            ac = ActionChains(dr)  # 这里创建新的ActionChains 目的是防止move_by_offset()的xoffset累加
            print(slider.location)
            all += track
        print("all=", all)
        time.sleep(0.5)
        for back_tracks in tracks['back_tracks']:  # 固定退19
            ac.move_by_offset(xoffset=back_tracks, yoffset=0).perform()
            ac = ActionChains(dr)
        # ActionChains(dr).move_by_offset(xoffset=-3, yoffset=0).perform()
        # print(slider.location)
        # ac.move_by_offset(xoffset=-6, yoffset=0).perform()
        # ac = ActionChains(dr)
        # ac.move_by_offset(xoffset=-4, yoffset=0).perform()
        # ac = ActionChains(dr)
        # ac.move_by_offset(xoffset=-2, yoffset=0).perform()
        # ac = ActionChains(dr)
        # ac.move_by_offset(xoffset=3, yoffset=0).perform()
        # print(slider.location)
        print(slider.location)
        ac.move_by_offset(xoffset=-8, yoffset=0).perform()
        print(slider.location)
        ac = ActionChains(dr)
        ac.move_by_offset(xoffset=5, yoffset=0).perform()
        print(slider.location)
        time.sleep(0.5)
        ac.release().perform()
        failure = None
        # wait = WebDriverWait(dr,5)
        time.sleep(5)
        failure = EC.text_to_be_present_in_element(("class name", 'yidun_tips__text'), '向右拖动滑块填充拼图')(dr)
        # print(failure)
        if not failure:
            print("验证成功！！")
            return True
        else:
            print("验证失败！")
            drag_block(dr)
            return True

def login_and_make_order(game,good_id,price):
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    dr = webdriver.Chrome(options=option)
    dr.maximize_window()
    dr.get("https://buff.163.com/")

    # dr.implicitly_wait(4)
    login = dr.find_element_by_link_text("登录")
    login.click()
    time.sleep(2)
    dr.switch_to.frame(dr.find_element_by_xpath("/html/body/div[7]/div[2]/div[1]/div[1]/iframe"))

    tab0 = dr.find_element_by_link_text("使用密码验证登录")
    dr.execute_script("arguments[0].click();", tab0)  #这里用tab0.click()不能正常点击

    phoneipt = dr.find_element_by_id("phoneipt")
    phoneipt.send_keys("17600870550")  #这里用firefox浏览器无法输入，用chrome解决

    password = dr.find_element_by_class_name("j-inputtext")
    password.send_keys("1997ye1152009")


    time.sleep(2)
    result = drag_block(dr)
    if result:
        time.sleep(1)
        submitBtn = dr.find_element_by_id("submitBtn")
        submitBtn.click()
        time.sleep(2)
        dr.get("https://buff.163.com/market/goods?goods_id="+good_id+"&from=market#tab=selling")   #加个价格比对
        time.sleep(2)
        try:
            now_price = float(dr.find_element_by_xpath("/html/body/div[6]/div[1]/div[5]/table/tbody/tr[2]/td[6]/strong").text[1:])
            print(now_price)
        except:
            now_price = float(dr.find_element_by_xpath("/html/body/div[6]/div[1]/div[4]/table/tbody/tr[2]/td[6]/strong").text[1:])
            print(now_price)
        if now_price != price:
            print("价格异常！")
            return 2
        buy_btn = dr.find_element_by_xpath("/html/body/div[6]/div[1]/div[5]/table/tbody/tr[2]/td[7]/a")
        buy_btn.click()
        time.sleep(2)
        make_order_btn = dr.find_element_by_class_name("pay-btn")
        make_order_btn.click()
        time.sleep(3)
        dr.close()
        return 0
    else:
        print("error!")
        return 1


# if __name__ == "__main__":
#     main()
#     print("完成！")
#     while True:
#         pass


# 260   380