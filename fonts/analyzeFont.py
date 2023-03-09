#!/usr/bin/env python3
from PIL import Image
import numpy as np
import pickle

def score(imgArr):
	scores = {}
	for i in range(32,127):
		chrImg = imgArr[:,(9*(i-32)):(9*(i-31)),:]
		score = chrImg.sum()
		scores[score] = chr(i)
	return scores

def main():
	print("Special formatting for png image file required. 9 pixel wide characters, ASCII codes 32-126 in image")
	imgName = input("Enter the png image file name (not including the extension)> ")
	img = Image.open(imgName + ".png")
	npImg = np.array(img)
	
	print(npImg.shape)
	
	scores = score(npImg)
	print(scores)

	with open(imgName + ".pkl", "wb") as file:
		pickle.dump(scores,file)
	
	print("Scores Written")

if __name__ == "__main__":
	main()
