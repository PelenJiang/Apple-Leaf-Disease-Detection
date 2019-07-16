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
sourcePicture = r'./Sources'
augumentPicture = "Augumentation"
saveDir = ""
def getPictureList():
    # set up output dir
    if not os.path.exists(r'./Augumentation'):
        os.mkdir(r'./Augumentation')
    
    for category in os.listdir(r'./Sources'):
    #for category in ["2"]:
        global saveDir
        saveDir = os.path.join(r'./Augumentation', category)
        #self.outDir = r'./Lables'
        print("正在处理类别"+category+"...")
        if not os.path.exists(saveDir):
            os.mkdir(saveDir)
        sourceCategoryPath = os.path.join(sourcePicture,category)
        sourceImageList = glob.glob(os.path.join(sourceCategoryPath, '*'))
        for sourceImage in sourceImageList:
            im = Image.open(sourceImage)
            im = im.resize((512,512))
            newFileName = os.path.splitext(os.path.basename(sourceImage))[0] + ".jpg"
            picture = os.path.join(saveDir,newFileName)
            im.save(os.path.join(saveDir,newFileName))
            
            brightnessTransfer(picture)
            contrastTransfer(picture)
            sharpnessTransfer(picture)
            
            PCAJitteringTransfer(picture)
            
            rotateTransfer(picture)
            flipTransfer(picture)
            gaussianTransfer(picture)
            
    print("处理完成")   
def brightnessTransfer(picture):#亮度
    image = Image.open(picture)
    enhancer = ImageEnhance.Brightness(image)
    #image2 = image.rotate(60)
    factor = 0.5
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_brightness_1.jpg"
    enhancedImage = enhancer.enhance(factor)
    enhancedImage = enhancedImage.save(os.path.join(saveDir,newFileName))
    
    factor = 1.5
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_brightness_2.jpg"
    enhancedImage = enhancer.enhance(factor)
    enhancedImage = enhancedImage.save(os.path.join(saveDir,newFileName))
    #for i in range(3):
        #factor = (i+1) / 2.0
        #enhancedImage = enhancer.enhance(factor).show("brightness %f" % factor)
        #newFileName = os.path.splitext(os.path.basename(picture))[0] + "_brightness_" + str(i)+".jpg"
       #enhancedImage = enhancer.enhance(factor)
        #print(saveDir)
        #enhancedImage = enhancedImage.save(os.path.join(saveDir,newFileName))
def contrastTransfer(picture):#对比度
    image = Image.open(picture)
    enhancer = ImageEnhance.Contrast(image)
    #image2 = image.rotate(60)
    #for i in range(4):
     #   factor = (i+1) / 2.0
     #   enhancer.enhance(factor).show("contrast %f" % factor)
    factor = 0.5
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_contrast_1.jpg"
    enhancedImage = enhancer.enhance(factor)
    enhancedImage = enhancedImage.save(os.path.join(saveDir,newFileName))
    
    factor = 1.5
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_contrast_2.jpg"
    enhancedImage = enhancer.enhance(factor)
    enhancedImage = enhancedImage.save(os.path.join(saveDir,newFileName))

def sharpnessTransfer(picture):#锐化度
    image = Image.open(picture)
    enhancer = ImageEnhance.Sharpness(image)
    #image2 = image.rotate(60)
    #for i in range(4):
    #    factor = (i+1) / 2.0
    #    enhancer.enhance(factor).show("Sharpness %f" % factor)
    factor = 0.5
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_sharpness_1.jpg"
    enhancedImage = enhancer.enhance(factor)
    enhancedImage = enhancedImage.save(os.path.join(saveDir,newFileName))
    
    factor = 1.5
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_sharpness_2.jpg"
    enhancedImage = enhancer.enhance(factor)
    enhancedImage = enhancedImage.save(os.path.join(saveDir,newFileName))

def PCAJitteringTransfer(picture):#PCA Jittering
    img = Image.open(picture)
    img = np.asarray(img,dtype = 'float32')
    img = img/255.
    img_size = img.size/3
    img1 = img.reshape(int(img_size),3)
    img1 = np.transpose(img1)      
    img_cov = np.cov([img1[0],img1[1],img1[2]])
    lamda,p = np.linalg.eig(img_cov)
    #分别对应特征值与特征向量组成的向量，结果是已经排序的。
    p = np.transpose(p)
    
    alpha1 = random.normalvariate(0,3)
    alpha2 = random.normalvariate(0,3)
    alpha3 = random.normalvariate(0,3)
    v = np.transpose((alpha1*lamda[0],alpha2*lamda[1],alpha3*lamda[2]))
    
    add_num = np.dot(p,v)
    
    img2 = np.array([img[:,:,0]+add_num[0],img[:,:,1]+add_num[1],img[:,:,2]+add_num[2]])
    
    img2 = np.swapaxes(img2,0,2)
    img2 = np.swapaxes(img2,0,1)
    #misc.imsave("./test2.jpg",img2)
    
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_PCA_1.jpg"
    misc.imsave(os.path.join(saveDir,newFileName),img2)
def rotateTransfer(picture):#旋转图片
    img = Image.open(picture)
    #img.show()
    img2 = img.rotate(90)
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_rotate_1.jpg"
    img2.save(os.path.join(saveDir,newFileName))
    
    img2 = img.rotate(180)
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_rotate_2.jpg"
    img2.save(os.path.join(saveDir,newFileName))
    
    img2 = img.rotate(270)
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_rotate_3.jpg"
    img2.save(os.path.join(saveDir,newFileName))


def flipTransfer(picture):
    img = Image.open(picture)
    #img.show()
    x=img.size[0]  
    y=img.size[1] 
    img=img.load()
    c = Image.new("RGB",(x,y))
    d = Image.new("RGB",(x,y))
    
    for i in range (0,x):  
        for j in range (0,y):  
            w=x-i-1  
            h=y-j-1  
            rgb=img[w,j] #镜像翻转  
            #rgb=img[w,h] #翻转180度  
            #rgb=img[i,h] #上下翻转  
            rgb2 = img[i,h]#上下翻转
            c.putpixel([i,j],rgb)
            d.putpixel([i,j],rgb2)
    #c.show()
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_flip_1.jpg"
    c.save(os.path.join(saveDir,newFileName))
    
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_flip_2.jpg"
    d.save(os.path.join(saveDir,newFileName))

'''
def gaussianTransfer(picture):
    img = Image.open(picture)
    #img.show()
    im=img.filter(ImageFilter.GaussianBlur(radius=2))
    #im.show()
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_gaussian_1.jpg"
    im.save(os.path.join(saveDir,newFileName))
    
    im=img.filter(ImageFilter.GaussianBlur(radius=3))
    #im.show()
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_gaussian_2.jpg"
    im.save(os.path.join(saveDir,newFileName))
    
    im=img.filter(ImageFilter.GaussianBlur(radius=4))
    #im.show()
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_gaussian_3.jpg"
    im.save(os.path.join(saveDir,newFileName))
 '''
def gaussianTransfer(picture):
    
  
    def gaussianNoisy(im, mean=0.2, sigma=0.3):

        for _i in range(len(im)):
            im[_i] += random.gauss(mean, sigma)
        return im

    # 将图像转化成数组
    mean = 0.2
    sigma = 0.3
    image = Image.open(picture)
    img = np.asarray(image)
    img.flags.writeable = True  # 将数组改为读写模式
    width, height = img.shape[:2]
    img_r = gaussianNoisy(img[:, :, 0].flatten(), mean, sigma)
    img_g = gaussianNoisy(img[:, :, 1].flatten(), mean, sigma)
    img_b = gaussianNoisy(img[:, :, 2].flatten(), mean, sigma)
    img[:, :, 0] = img_r.reshape([width, height])
    img[:, :, 1] = img_g.reshape([width, height])
    img[:, :, 2] = img_b.reshape([width, height])
    saveImage = Image.fromarray(np.uint8(img))
    newFileName = os.path.splitext(os.path.basename(picture))[0] + "_gaussian_1.jpg"
    saveImage.save(os.path.join(saveDir,newFileName))
       
if __name__ == '__main__':
    getPictureList()
    #picture = "test.jpg"
    #brightnessTransfer(picture)
    #contrastTransfer(picture)
    #sharpnessTransfer(picture)
    #PCAJitteringTransfer(picture)
    #rotateTransfer(picture)
    #flipTransfer(picture)
    #gaussianTransfer(picture)
