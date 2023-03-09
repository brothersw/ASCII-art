#!/usr/bin/env python3
from PIL import Image
import numpy as np
import pickle

#scores individual pixels for luminosity
def scoreImage(npImg):
	scoreArr = np.zeros((npImg.shape[:2]), dtype=int)
	for x,y in np.ndindex(npImg.shape[:2]):
		scoreArr[x,y] = np.sum(npImg[x,y,:])
	return scoreArr

#groups pixels into blocks for large images
def groupPixels(scoreArr, xBlock, yBlock):
	shape = scoreArr.shape
	assert shape[0]>=yBlock and shape[1]>=xBlock, "The total size should be greater than the block size"
	
	ySize = int(scoreArr.shape[0]/yBlock)
	xSize = int(scoreArr.shape[1]/xBlock)
	outArr = np.zeros([ySize, xSize])
	
	print(outArr.shape)	
	for i in range(ySize):
		for j in range(xSize):
			# calculate the average of the block
			block = scoreArr[i*yBlock:(i+1)*yBlock, j*xBlock:(j+1)*xBlock]
			avg = np.mean(block)
			# assign the average to the output array
			outArr[i][j] = int(avg)
    
	return outArr

#loads pickle font dictionary
def loadFont(fontFile):
	data = {}
	with open(fontFile, "rb") as file:
		data = pickle.load(file)
	return data

#level to font range so that image isn't obscured
def levelImage(scoreArr, fontScores):
	scoreMax = np.amax(scoreArr)
	fontMax = max(fontScores.keys())
	scaleRatio = fontMax/scoreMax
	return scoreArr * scaleRatio

#match score to closest dictionary key
def matchScore(score, fontScores):
    closest = min(fontScores.keys(), key=lambda x: abs(x - score))
    return fontScores[closest]

#loop over output scores to print image
def printArt(scoreArr, fontScores):
	for y in scoreArr:
		row = ""
		for x in y:
			row += matchScore(x, fontScores)
		print(row)

def main():
	imgFile = input("Enter the PNG image file name> ")
	img = Image.open(imgFile)
	npImg = np.array(img)
	
	scoreArr = scoreImage(npImg)
	scoreArr = groupPixels(scoreArr, 9,16)
	fontScores = loadFont("UbuntuMono.pkl") #set me if generated new font
	scoreArr = levelImage(scoreArr, fontScores)
	printArt(scoreArr, fontScores)

if __name__ == "__main__":
	main()
