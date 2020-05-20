# coding=utf-8
import argparse
import json
import numpy as np 
import lipColor 
import os, sys

parser = argparse.ArgumentParser(description='lip color matching')
parser.add_argument('data', metavar='DIR', help='path to dataset')
parser.add_argument('image', metavar='DIR', help='path to source image dir')
parser.add_argument('-N', '--number', default=3, type=int, metavar='N',
					help='number of best matching (defult: 3)')

 

class Dataset:
    def __init__(self, json_path):
        
        self._ret_dic = {}  #json
        self._series_list=[]
        self._brands_num = 0
        self._color_num_sum = 0
        self._data_list = [] # 口红信息
        self._RGB_array = [] # 口红色号RGB

        # load_data
        with open(json_path, 'r', encoding='utf-8') as f: 
            self._ret_dic = json.load(f) 
        self._brands_num=len(self._ret_dic['brands']) 
        #series brands# 
        for i in range(self._brands_num): 
            s_num=len(self._ret_dic['brands'][i]['series']) 
            self._series_list.append(s_num)     
        self._color_num_sum = self.get_color_num_sum()
        self._data_list, self._RGB_array = self.get_list()

    def get_color_num_sum(self):
        color_num_sum =0 
        for brand in range(self._brands_num): 
            for series in range(self._series_list[brand]): 
                color_num = len(self._ret_dic['brands'][brand]['series'][series]['lipsticks']) 
                color_num_sum += color_num #calculate the total color numbers 
        return color_num_sum

    """
    将信息转化为list形式
    """
    def get_list(self):
        data_list = []
        RGB_array = []

        for brand in range(self._brands_num): 
            for series in range(self._series_list[brand]): 
                brand_name = self._ret_dic['brands'][brand]['name'] 
                lip_name = self._ret_dic['brands'][brand]['series'][series]['name'] 
                color_num = len(self._ret_dic['brands'][brand]['series'][series]['lipsticks']) 
                
                for c in range(color_num): 
                    color_value=self._ret_dic['brands'][brand]['series'][series]['lipsticks'][c]['color'] 
                    color_name=self._ret_dic['brands'][brand]['series'][series]['lipsticks'][c]['name'] 
                    color_id=self._ret_dic['brands'][brand]['series'][series]['lipsticks'][c]['id'] 
                    
                    lip_info = {'brand':brand_name, 'lip':lip_name, 'color_name':color_name,'color_id': color_id}
                    data_list.append(lip_info)
                    RGB_array.append(convertValue2RGB(color_value))
        return data_list, RGB_array
    def getData(self):
        return self._color_num_sum, self._data_list, self._RGB_array


"""
#D62352 ->  [214, 35, 82]
value   ->  RGB
"""
def convertValue2RGB(color_value):
    RGB = []
    for i in range(3):
        index = (i << 1) + 1
        temp = color_value[index:index + 2]
        value = int(temp,16)
        RGB.append(value)
    return RGB

def getDistance(A, B):
    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)
    return np.linalg.norm(A - B)    

def findSimilarColor(color_num_sum, RGB_array, A, N = 3):
    #calculate the similar and save to RGB_temp 
    #RGB_temp=np.zeros((sum,1), dtype=int) 
    RGB_temp=np.zeros((color_num_sum,1), dtype=float) 
    for i in range(color_num_sum): 
        RGB_temp[i]= getDistance(A, RGB_array[i]) 
    
    RGB_temp.tolist()
    #sort the RGB_temp# 
    result=sorted(range(len(RGB_temp)), key=lambda k: RGB_temp[k]) 
    if N < color_num_sum:
        return result[0: N + 1]
    else:
        return result
 
def findBestMatch(args):
    data_path = args.data
    color_dir = args.image
    N = args.number


    count, dir_list= lipColor.load_color(color_dir, []) 
    image= lipColor.Mean_color(count,dir_list) 
    
    print("the extracted RGB value of the color is {0}".format(image)) 

    data = Dataset(data_path)
    color_num_sum, data_list, RGB_array = data.getData()
    result = findSimilarColor(color_num_sum, RGB_array, image, N)
        #output the three max prob of the lipsticks# 
    print("The first three possible lipstick brand and color id&name are as follows:") 
    for i in result:  
        print(data_list[i]) 
    print("The first three possible lipstick brand RGB value are as follows:") 
    for i in result:  
        R=RGB_array[i][0] 
        G=RGB_array[i][1] 
        B=RGB_array[i][2] 
        tuple=(R,G,B) 
        print(tuple)    
    return result

def main():
    args = parser.parse_args()
    findBestMatch(args)
if __name__ == '__main__': 
    main()
    