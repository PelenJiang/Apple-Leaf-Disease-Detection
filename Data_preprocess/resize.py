# -*- coding: utf-8 -*-
from PIL import ImageEnhance
from PIL import Image
import numpy as np
import os
import os.path
from PIL import Image,ImageOps,ImageFilter
import random
from scipy import misc
import glob



def resize():
    for a in os.listdir(r'./Sources'):
        imageDir = os.path.join(r'./Sources', a)
        print(imageDir)
        imageList = glob.glob(os.path.join(imageDir, '*'))
        if len(imageList) == 0:
            print ('No images found in the specified dir!')
            return   
        for idx in imageList:
            im = Image.open(idx)
            print (im.format, im.size, im.mode)
            out = im.resize((500,500))
            newname=os.path.splitext(os.path.basename(idx))[0]+ ".jpg"
            newDir=os.path.join(r'./Pretreats/',a)      
            out.save(os.path.join(newDir, newname))

if __name__ == '__main__':
#    im = Image.open("test.jpg")
#   print (im.format, im.size, im.mode)
#    im.show()
#    out = im.resize((225,225))
#    out.show()
#    out.save("test_bak.jpg")
    resize()