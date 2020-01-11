# -*-coding=utf-8-*-
import requests
import pytesseract
import cv2
import time
import re
import csv
import schedule

def job(srcs):
    print('上次保存图片中的时间数据：',datetimes)
    for index, src in enumerate(srcs):
    #for index,src,spot in zip(enumerate(srcs),spots):
        Time = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
        print(Time)
        imgName = Time + ".jpg"
        response = requests.get(src)
        with open(imgName, "wb") as f:
            f.write(response.content)
        img = cv2.imread(imgName)
        shape = img.shape
        img = cv2.resize(img,(shape[1]*3,shape[0]*3)) #图片尺寸扩大5倍。便于识别
        cv2.imwrite(imgName,img)
        text = pytesseract.image_to_string(img,lang='chi_sim')
        print(text)
        text= re.findall(r'\d+',text)
        current_level = text[0]+'.'+text[1]
        warning_level = text[2]+'.'+text[3]
        nowtime = text[4]+'-'+text[5] + '_' + text[6]+':'+text[7]
        if datetimes[int(index)] == nowtime:
            print("时间一致，正在跳过...")
            continue
        else:
            print("检测到新数据，正在写入...")
            datetimes[int(index)] = nowtime
        datas = [spots[index],nowtime,current_level,warning_level]
        with open('water.csv', "a+", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(datas)
            f.close()

if __name__ == '__main__':
    srcs = ['http://221.226.28.67:88/jsswxxSSI/static/map1/0/3/b65dc75abebc407ead1ae9d632c85e4d.png',
            'http://221.226.28.67:88/jsswxxSSI/static/map1/0/3/a96709f810214c53b6234f4530689655.png']
    spots = ['双沟', '尚咀']
    datetimes = ['','']
    schedule.every(10).seconds.do(job,srcs)  # 10秒钟执行一次
    #schedule.every(10).minutes.do(job,src)  # 10分钟执行一次
    #schedule.every().hour.do(job,src)  # 每个小时执行一次
    while True:
        schedule.run_pending()
        #print(schedule.idle_seconds())

