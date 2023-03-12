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

#Auto scales text blocks from original image size
#(2,1) text ratio for looking nice
def scaleImage(imgShape, totalWidth):
    x = int(imgShape[1] / totalWidth)
    y = int(imgShape[0] / (totalWidth * 0.5))
    return x, y

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

#loop over output scores to return image string
def getArt(scoreArr, fontScores):
	out = ""
	for y in scoreArr:
		for x in y:
			out += matchScore(x, fontScores)
		out += "\n"
	return out

def controlOverview(npImg, outWidth, fontFile):
	scoreArr = scoreImage(npImg)
	blocks = scaleImage(scoreArr.shape, outWidth)
	scoreArr = groupPixels(scoreArr, blocks[0], blocks[1])
	fontScores = loadFont(fontFile)
	scoreArr = levelImage(scoreArr, fontScores)
	return getArt(scoreArr, fontScores)

def main():
	imgFile = input("Enter the PNG image file name> ")
	outWidth = int(input("How many characters wide do you want the output> "))
	img = Image.open(imgFile)
	npImg = np.array(img)
	
	print(controlOverview(npImg, outWidth, "UbuntuMono.pkl"))

if __name__ == "__main__":
	main()
