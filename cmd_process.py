# -*- coding: utf-8 -*-
"""
Created on Sun May  8 13:30:44 2022

@author: 10366073
"""

import os , shutil , add_information

def upload(data_path , Author , title):#路徑、上傳者、標題
    
    i = add_information.count() +1
    
    data_path = data_path.replace("\\", "/")
    
    data_path = data_path.replace('"', "")
    
    mpd_name = str(i)
    
    add_information.add_new_video(str(i) , title , "http://180.218.7.38/{0}.mpd".format(i) , Author)
    
    cmd = [
           "ffmpeg -i {0} -s 160x90 -c:v libx264 -b:v 250k -g 90 -an D:/data/{1}_160x90_250k.mp4".format(data_path , i),
           "ffmpeg -i {0} -s 320x180 -c:v libx264 -b:v 500k -g 90 -an D:/data/{1}_320x180_500k.mp4".format(data_path , i),
           "ffmpeg -i {0} -s 640x360 -c:v libx264 -b:v 750k -g 90 -an D:/data/{1}_640x360_750k.mp4".format(data_path , i),
           "ffmpeg -i {0} -s 640x360 -c:v libx264 -b:v 1000k -g 90 -an D:/data/{1}_640x360_1000k.mp4".format(data_path , i),
           "ffmpeg -i {0} -s 1280x720 -c:v libx264 -b:v 1500k -g 90 -an D:/data/{1}_1280x720_1500k.mp4".format(data_path , i),
           "ffmpeg -i {0} -c:a aac -b:a 128k -vn D:/data/{1}_audio__128k.mp4".format(data_path , i),
           "mp4box -dash 5000 -rap -profile dashavc264:onDemand -mpd-title {0} -out D:/data/{1}.mpd -frag 2000 D:/data/{1}_audio__128k.mp4 D:/data/{1}_160x90_250k.mp4 D:/data/{1}_320x180_500k.mp4 D:/data/{1}_640x360_750k.mp4 D:/data/{1}_640x360_1000k.mp4 D:/data/{1}_1280x720_1500k.mp4".format(mpd_name,i)
          ]
    
    for i in range(0,7,1):
        os.system("{0}".format(cmd[i]))
