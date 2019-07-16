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



def changename():
        imageList = glob.glob(os.path.join(r'./Pretreats/5', '*'))
        if len(imageList) == 0:
            print ('No images found in the specified dir!')
            return
        myNum=20683
        for idx in imageList:
            im = Image.open(idx)
            print (im.format, im.size, im.mode)
            myName = "%06d" % myNum
            myNum +=1
            newname=str(myName)+ ".jpg"   
            im.save(os.path.join('./Rename', newname))

if __name__ == '__main__':
    print ('开始处理')
    changename()
    print ('处理完成')