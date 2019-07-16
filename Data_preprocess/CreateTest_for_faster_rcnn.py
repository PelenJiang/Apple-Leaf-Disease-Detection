# -*- coding: utf-8 -*-
import os
import sys
import random
import shutil

try:
    #start = int(sys.argv[1])
    #end = int(sys.argv[2])
    #test = int(sys.argv[3])
    #allNum = end-start+1
    start = 1
    end = 26377
    trainval = 21102
    test = 5275
    val = 5275
    train = 15827
    allNum = 26377
except:
    print ('Please input picture range')
    print ('./createTest.py 1 1500 500')
    os._exit(0)

list = range(start,end)
trainval_list = random.sample(list, trainval)
trainval_list = sorted(trainval_list) 
train_list = random.sample(trainval_list, train)
train_list = sorted(train_list) 
allFile = []

imageSetsdir = os.path.join(os.getcwd(),"ImageSets")
if  os.path.exists(imageSetsdir):
    shutil.rmtree(imageSetsdir)
os.mkdir(imageSetsdir)

maindir = os.path.join(imageSetsdir,"Main")
if  os.path.exists(maindir):
    shutil.rmtree(maindir)
os.mkdir(maindir)

testFile = open('ImageSets/Main/test.txt', 'w')
trainFile = open('ImageSets/Main/train.txt', 'w')
valFile = open('ImageSets/Main/val.txt', 'w')
trainvalFile = open('ImageSets/Main/trainval.txt', 'w')

for i in list:
    name="%06d" % (i-1)
    if i in trainval_list:
        trainvalFile.write(name + '\n')
        if i in train_list:
            trainFile.write(name + '\n')
        else:
            valFile.write(name + '\n')
    else:
        testFile.write(name + '\n')

testFile.close()
trainFile.close()
valFile.close()
trainvalFile.close()