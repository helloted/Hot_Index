#coding=utf-8

import os
import shutil


# def move_file():
#     for filename in os.listdir('ts'):
#         if filename[-2:] == 'ts':
#             src = 'ts/' + filename
#             tar = 't/' + filename
#             shutil.move(src,tar)

def move_file(old,new):
    for filename in os.listdir(old):
        if filename[-2:] == 'ts':
            src = old + '/' + filename
            tar = new+ '/' + filename
            shutil.move(src, tar)

def move_to_all():
    super_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    all_folder = super_path+'/all'
    if not os.path.exists(all_folder):
        os.makedirs(all_folder)
    dirs = os.listdir(super_path)
    for dir in dirs:
        if dir[1:3] == '00':
            move_file(dir,'all')

def make_file_list():
    list = os.listdir('all')
    list = filter(lambda x: x[-2:] == 'ts', list)
    list.sort(key=lambda x:int(x[:-3]))
    with open('all/filelist.txt','w') as file:
        for i,filename in enumerate(list):
            if i < 5 or i > len(list) - 6:
                pass
            else:
                file.write('file '+filename + '\n')


if __name__ == '__main__':
    move_to_all()
    make_file_list()
    os.system('ffmpeg -f concat -i all/filelist.txt -acodec copy -vcodec copy -f mp4 cat.mp4')

