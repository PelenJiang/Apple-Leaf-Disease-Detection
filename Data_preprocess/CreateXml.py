# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
#import cv2
from PIL import Image
from itertools import islice
from xml.dom.minidom import Document
import shutil

pLabels='Labels'
labels='labels'
imgpath='JPEGImages'
#imgpath='JPEGImages/'
xmlpath_new='Annotations'
foldername='VOC2007'
pretreat='Pretreats/'


def insertObject(doc, L,i):
    obj = doc.createElement('object')
    name = doc.createElement('name')
    name.appendChild(doc.createTextNode(str(L[i][0])))
    obj.appendChild(name)
    pose = doc.createElement('pose')
    pose.appendChild(doc.createTextNode('Unspecified'))
    obj.appendChild(pose)
    truncated = doc.createElement('truncated')
    truncated.appendChild(doc.createTextNode(str(0)))
    obj.appendChild(truncated)
    difficult = doc.createElement('difficult')
    difficult.appendChild(doc.createTextNode(str(0)))
    obj.appendChild(difficult)
    bndbox = doc.createElement('bndbox')
    
    xmin = doc.createElement('xmin')
    xmin.appendChild(doc.createTextNode(str(L[i][1])))
    bndbox.appendChild(xmin)
    
    ymin = doc.createElement('ymin')                
    ymin.appendChild(doc.createTextNode(str(L[i][2])))
    bndbox.appendChild(ymin)                
    xmax = doc.createElement('xmax')                
    xmax.appendChild(doc.createTextNode(str(L[i][3])))
    bndbox.appendChild(xmax)                
    ymax = doc.createElement('ymax')    
    if  '\r' == str(L[i][4])[-1] or '\n' == str(L[i][4])[-1]:
        data = str(L[i][4])[0:-1]
    else:
        data = str(L[i][4])
    ymax.appendChild(doc.createTextNode(data))
    bndbox.appendChild(ymax)
    obj.appendChild(bndbox)                
    return obj

def create():
    indexNum = 0#数字下标
    #print (os.getcwd()) E:\JAVA\NewWorkSpace\ApplePests\DataSetPretreat
    #if path exist return true else false ,function join merge dir path and file path 
    #os.getcwd()return current path
    if  os.path.exists(os.path.join(os.getcwd(),imgpath)):#JPEGImages
        shutil.rmtree(imgpath)#delete dir and file
    if  os.path.exists(os.path.join(os.getcwd(),xmlpath_new)):#Annotation
        shutil.rmtree(xmlpath_new)
    os.mkdir(os.path.join(os.getcwd(),imgpath))#make new dir
    os.mkdir(os.path.join(os.getcwd(),xmlpath_new))
    for category in os.listdir(labels):#return all file names
        labelCategoryPath = os.path.join(labels,category)
        pretreatCategoryPath = os.path.join(pretreat,category)
        for label in os.listdir(labelCategoryPath):
            pictureName = label.replace('.txt', '.jpg')#预处理的图片名
            indexName = "%06d" % indexNum#新文件名称
            picturePathIndexName = os.path.join(imgpath,indexName+".jpg")#新图片路径
            pretreatPicturePath = os.path.join(pretreatCategoryPath,pictureName)#预处理的图片路径
            #拷贝文件并命名为pictureIndexName.jpg
            shutil.copy(pretreatPicturePath,picturePathIndexName)
            #open(picturePathIndexName, "wb").write(open(pretreatPicturePath, "rb").read())
            fidin=open(labelCategoryPath + '/'+ label,'r')
            objIndex = 0
            L=[]
            for data in islice(fidin, 1, None):        
                objIndex += 1
                data=data.strip('\n')
                datas = data.split(' ')
                if 5 != len(datas):
                    print ('bounding box information error')
                    continue
                L.append(datas)
            #imageFile = imgpath + pictureName
            #img = cv2.imread(imageFile)
            img = Image.open(picturePathIndexName)
            imgSize = img.size
            imgSize = imgSize + (3,)
            #xmlName = each.replace('.txt', '.xml')
            #f = open(xmlpath_new + indexName + ".xml", "w")
            f = open(os.path.join(xmlpath_new,indexName+".xml"), "w")
            doc= Document()
            annotation = doc.createElement('annotation')
            doc.appendChild(annotation)
                        
            folder = doc.createElement('folder')
            folder.appendChild(doc.createTextNode(foldername))
            annotation.appendChild(folder)
                        
            filename = doc.createElement('filename')
            filename.appendChild(doc.createTextNode(indexName+".jpg"))
            annotation.appendChild(filename)
                        
            source = doc.createElement('source')                
            database = doc.createElement('database')
            database.appendChild(doc.createTextNode('My Database'))
            source.appendChild(database)
            source_annotation = doc.createElement('annotation')
            source_annotation.appendChild(doc.createTextNode(foldername))
            source.appendChild(source_annotation)
            image = doc.createElement('image')
            image.appendChild(doc.createTextNode('flickr'))
            source.appendChild(image)
            flickrid = doc.createElement('flickrid')
            flickrid.appendChild(doc.createTextNode('NULL'))
            source.appendChild(flickrid)
            annotation.appendChild(source)
                        
            owner = doc.createElement('owner')
            flickrid = doc.createElement('flickrid')
            flickrid.appendChild(doc.createTextNode('NULL'))
            owner.appendChild(flickrid)
            name = doc.createElement('name')
            name.appendChild(doc.createTextNode('idaneel'))
            owner.appendChild(name)
            annotation.appendChild(owner)
                        
            size = doc.createElement('size')
            width = doc.createElement('width')
            width.appendChild(doc.createTextNode(str(imgSize[0])))
            size.appendChild(width)
            height = doc.createElement('height')
            height.appendChild(doc.createTextNode(str(imgSize[1])))
            size.appendChild(height)
            depth = doc.createElement('depth')
            depth.appendChild(doc.createTextNode(str(imgSize[2])))
            size.appendChild(depth)
            annotation.appendChild(size)
                        
            segmented = doc.createElement('segmented')
            segmented.appendChild(doc.createTextNode(str(0)))
            annotation.appendChild(segmented)
            for i in range(len(L)):            
                annotation.appendChild(insertObject(doc, L,i))
            try:
                f.write(doc.toprettyxml(indent = '    '))
                f.close()
                fidin.close()
            except:
                pass
            indexNum += 1
          
if __name__ == '__main__':
    create()
    #for dirnames in os.listdir(pLabels):
    #   print (dirnames)
