import colorsys 
import PIL.Image as Image
import os
from os.path import join as pjoin 
from scipy import misc

def get_dominant_color(image): 
    max_score = 0.0001 
    dominant_color = None 
    for count,(r,g,b) in image.getcolors(image.size[0]*image.size[1]): 
        # 转为HSV标准 
        saturation = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)[1] 
        y = min(abs(r*2104+g*4130+b*802+4096+131072)>>13,235) 
        y = (y-16.0)/(235-16) 
 
        #忽略高亮色 
        if y > 0.9: 
            continue 
        score = (saturation+0.1)*count 
        if score > max_score: 
            max_score = score 
            dominant_color = (r,g,b) 
    return dominant_color 

def load_color(color_dir, dir_list):  
    count = 0 
    for dir in os.listdir(color_dir):   
        img_dir = pjoin(color_dir, dir)   
        image = Image.open(img_dir) 
        image = image.convert('RGB') 
        get= get_dominant_color(image) 
        dir_list.append(get) 
        count = count+1 
        #print(person_dir) 
    #print(count) 
    return count, dir_list
 
def Mean_color(count,dir_list): 
    # 求平均值，缩减误差
     Mean_R=Mean_G=Mean_B=0 
     for i in range(count): 
        RGB = dir_list[i] 
        Mean_R+=RGB[0] 
        Mean_G+=RGB[1] 
        Mean_B+=RGB[2] 
     MeanC=((int)(Mean_R/count),(int)(Mean_G/count),(int)(Mean_B/count)) 
     return MeanC