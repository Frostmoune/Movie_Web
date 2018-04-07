# 这个包用于处理收集到的海报图片，可以不用管
from PIL import Image
import os
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

path = os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + "/"
tags = ['大陆电影','美国电影','香港电影','台湾电影','日本电影','韩国电影','英国电影','法国电影','德国电影','印度电影','泰国电影',
            '剧情','爱情','喜剧','科幻','动作','悬疑','犯罪','恐怖','青春','励志','战争','文艺','黑色幽默','传记','历史','情色','暴力',
            '音乐','家庭','经典','冷门佳片','魔幻','黑帮','女性']

def getPath(num):
    now_path = ""
    now_dir = 100000
    while now_dir>1 and num//now_dir==0:
        now_path += "0"
        now_dir //= 10 
    now_path += str(num)
    return now_path

def picture(begin, end, num):
    now_num = num
    for x in tags[begin:end]:
        flag = 0
        if os.path.exists(path + x + "/" + x + "_title.txt"):
            length = len(os.listdir(path + x))-2
            flag = 1
        else:
            length = len(os.listdir(path + x))-1
        for i in range(0,length):
            try:
                now_path = "0"
                if i<100:
                    now_path += "0"
                if i<10:
                    now_path += "0"
                now_path += str(i) + ".png"
                if os.path.exists(path + x + "/" + now_path[:-4] + ".jpg"):
                    continue
                # now_image = Image.open(path + x + "/" + now_path).convert("RGB")
                # now_image.resize((270, 400),Image.ANTIALIAS).save(path + "海报/" + getPath(now_num) + ".jpg")
                os.remove(path + x + "/" + now_path)
                now_num += 1
            except Exception as e:
                print(e)
        print("Save tag %s finished. The number is %d"%(x,now_num-1))
        if flag:
            os.remove(path + x + "/" + x + "_title.txt")

picture(0,35,0)

