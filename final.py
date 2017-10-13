#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, glob

from PIL import Image
from numpy import array
from pylab import *

from scipy.spatial import distance
from scipy import misc
from operator import itemgetter
import numpy as np

from Tkinter import *
import ttk
from PIL import Image, ImageTk

def ChangeTargetToTargetAddress(num):
	target = 'dataset/ukbench00'
	if 0 <= num and num < 10:
		target += '00'
	elif 10 <= num and num < 100:
		target += '0'
	target += str(num) + '.jpg'
	return target

def Mosaic(qname, n):

	def partitioning(pixel, X, Y, width, height):

		# temp = []
		R_list = []
		G_list = []
		B_list = []
		for x in range(Y, Y + height):
			for y in range(X, X + width):
				R, G, B = pixel[y,x]
				# print RGB
				# original pixel in small partitioning version
				R_list.append(R)
				G_list.append(G)
				B_list.append(B)
		R_list = array(R_list)
		G_list = array(G_list)
		B_list = array(B_list)
		# temp = array(temp)
		# temp_histo, bins = np.histogram(temp.ravel(),256,[0,256])
		R_histo, bins = np.histogram(R_list.ravel(),256,[0,256])
		G_histo, bins = np.histogram(G_list.ravel(),256,[0,256])
		B_histo, bins = np.histogram(B_list.ravel(),256,[0,256])
		return R_histo, G_histo, B_histo





	im_target = Image.open(qname)
	width, height = im_target.size
	pixel = im_target.load()
	# print pixel[639,479]

	width_s = width / int(n)
	height_s = height / int(n)
	#------------------------------------------------#
	# compute every histogram of images from dataset #
	#------------------------------------------------#

	shrink_ratio = (1 / float(n))
	fnumber = 0
	dataset_histo_list_R = []
	dataset_histo_list_G = []
	dataset_histo_list_B = []
	for fname in glob.glob('dataset/*.jpg'):
		fnumber += 1
		im = Image.open(fname)
		# small = misc.imresize(im, shrink_ratio)
		small = im.resize((width_s, height_s), Image.BILINEAR )
		temp_pixel = small.load()
		# print "small"
		# print small.shape
		# print small
		R_histo, G_histo, B_histo = partitioning(temp_pixel, 0, 0, width_s, height_s)

		# small_histo, bins = np.histogram(small.ravel(),256,[0,256])

		dataset_histo_list_R.append(R_histo)
		dataset_histo_list_G.append(G_histo)
		dataset_histo_list_B.append(B_histo)


	print "w",width
	print "h",height
	print "w_s", width_s
	print "h_s", height_s



	#---------------------------------------------------------------------------#
	# partition the input image into n parts, compute the histogram: temp_histo #	
	# compute the distance between 1 part of the input and the image in dataset #
	#---------------------------------------------------------------------------#

	result = []

	for x in range(width):
		for y in range(height):
			if ( (y % (height / int(n) ) == 0) and (x % (width / int(n) ) == 0)):
				#print "x: "+ str(x) + "   y:" + str(y)
				R_histo, G_histo, B_histo = partitioning(pixel, x, y, width_s, height_s)
				# print temp_histo

				# Manhattan distance
				fnum = -1
				min_dst = sys.maxint
				for i in range(fnumber):
					# Manhattan distance
					# dst = distance.cityblock(temp_histo, dataset_histo_list[i])
					#print "i = " + str(i) + "   dst: " + str(dst)
					dst_R = distance.cityblock(R_histo, dataset_histo_list_R[i])
					dst_G = distance.cityblock(G_histo, dataset_histo_list_G[i])
					dst_B = distance.cityblock(B_histo, dataset_histo_list_B[i])
					# dst_R = distance.euclidean(R_histo, dataset_histo_list_R[i])
					# dst_G = distance.euclidean(G_histo, dataset_histo_list_G[i])
					# dst_B = distance.euclidean(B_histo, dataset_histo_list_B[i])
					dst = dst_R + dst_B + dst_B
					# dst /= 3
					if(min_dst > dst):
						min_dst = dst
						fnum = i
				result.append(fnum)


				print "x: "+ str(x) + "   y:" + str(y) + "     min_dst: " + str(min_dst) + "   fnum: " + str(fnum)
				print "==============================="

	n = int(n)
	resultImg = Image.open(qname)
	for x in range(len(result)):
		tempImg = Image.open(ChangeTargetToTargetAddress(result[x]))
		small = tempImg.resize((width_s, height_s), Image.BILINEAR )
		# print width_s * (x/n),  height_s * (x%n)
		resultImg.paste(small, (width_s * (x/n) , height_s * (x%n)))
	resultImg.show()

def okButtonClick():
	if question.current() == -1 and target.current() == -1:
		info.config(text='Please Select Num of Sides And Target !!!!!!!!')
	elif question.current() == -1:
		info.config(text='Please Select Num of Sides Thank You :D')
	elif target.current() == -1:
		info.config(text='Please Select Target Thank You :D')
	else:
		info.config(text='Now is Processing !!!! Please Wait:D')
		okButton.state(['disabled'])
		Mosaic(ChangeTargetToTargetAddress(target.current()), questionArray[question.current()])
		okButton.state(['!disabled'])
		info.config(text='Result is showing !')

targetArray = [x for x in range(1000)]
questionArray = ['2', '4', '8', '16', '40', '80', '160']

root = Tk()
root.title("MM_FinalProject_Mosaic")

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Num of Sides:").grid(row=0,column=0)
question = ttk.Combobox(mainframe, textvariable="")
question.grid(row=0,column=1)
question['values'] = questionArray

ttk.Label(mainframe, text="Target:").grid(row=1,column=0)
target = ttk.Combobox(mainframe, textvariable="")
target.grid(row=1,column=1)
target['values'] = targetArray

okButton = ttk.Button(mainframe, text='Okay' , command=okButtonClick)
okButton.grid(row=0,column=2, rowspan=2)

info = ttk.Label(mainframe, text="Please Select Num of Sides And Target")
info.grid(row=0,column=3,columnspan=2,rowspan=2)

root.mainloop()