import cv2
import os
import json
import time
import requests
import traceback
import numpy as np
from colormath.color_diff import delta_e_cie1976
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color

name = "canvas"

def check_image():
    global name
    if os.path.isfile(name+".jpg") == True or os.path.isfile(name+".png") == True:
        print('Found image!')
        return True
    elif name.startswith('http') and (name.endswith('.jpg') or name.endswith('.png')):
        print('Downloading image from', name)
        try:
            fileName = name.split('/')[-1][:10]

            with open(fileName, 'wb') as handle:
                print(fileName)
                response = requests.get(name)
                if not response.ok:
                    print('Could not download image:',response)
                    return False
                else:
                    handle.write(response.content)
                    name = fileName
                    return True
        except:
            traceback.print_exc()
            print('Could not download image: Invalid URL')
            return False
    else:
        print('Image not found!')
        return False

def ColorDistance(rgb1,rgb2):
    # Reference color.
    color1 = convert_color(sRGBColor(rgb1[0],rgb1[1],rgb1[2]), LabColor, target_illuminant='d50')
    # Color to be compared to the reference.
    color2 = convert_color(sRGBColor(rgb2[0],rgb2[1],rgb2[2]), LabColor, target_illuminant='d50')
    # This is your delta E value as a float.
    return delta_e_cie1976(color1, color2)

def changeColors(imageB):
    image = imageB.copy()
    rows,cols = image.shape[:2]

    for i in range(rows):
        for j in range(cols):
            k = image[i,j].tolist()
            distances = []
            toSearch = []
            for color in colors:
                color = colors.get(color)
                dist = ColorDistance(k,color)
                distances.append(dist)
                toSearch.append(color)
            closest = distances.index(min(distances))
            image[i,j] = toSearch[closest]
    return image
            #print(toSearch[closest])

f = open('dict.json','r')
colors = json.loads(f.read())
f.close()

while True:
    name = input('\nWhat is the name of the image (jpg,png only)?: ')
    if check_image() == False:
        continue
    else:
        break

# Input image
if os.path.isfile(name+".jpg"):
    img = cv2.imread(name+'.jpg')
elif os.path.isfile(name+".png"):
    img = cv2.imread(name+'.png')
else:
    img = cv2.imread(name)

# Get input size
height, width = img.shape[:2]

squared = input("Is your image a square (y/n)? ").lower()
if squared == "y":
    while True:
        pI = input('What pixel intensity do you want your image (integer)?: ')
        try:
            pI = int(pI)
        except:
            continue
        #Width
        w = round(pI)
        #Height
        h = round(pI)
        temp = cv2.resize(img, (w, h), interpolation=cv2.INTER_LINEAR)
        totalPixels = 0
        rows,cols = temp.shape[:2]
        for i in range(rows):
            for j in range(cols):
                totalPixels += 1
        print("\nYour LEGO canvas will be",w,"studs wide,",h,"studs high, with",totalPixels,"total studs")
        if input('Would you like to continue (y/n)? ').lower() == "y":
            break
else:
    while True:
        pI = input('What pixel intensity do you want your image (integer)?: ')
        try:
            pI = int(pI)
        except:
            continue
        #Width
        w = round(width / pI)
        #Height
        h = round(height / pI)
        temp = cv2.resize(img, (w, h), interpolation=cv2.INTER_LINEAR)
        totalPixels = 0
        rows,cols = temp.shape[:2]
        for i in range(rows):
            for j in range(cols):
                totalPixels += 1
        print("\nYour LEGO canvas will be",w,"studs wide,",h,"studs high, with",totalPixels,"total studs")
        if input('Would you like to continue (y/n)? ').lower() == "y":
            break

for color in colors:
    colors[color].reverse() # change to BGR color

print('\nReading',totalPixels,"pixels...\n")
previous = time.time()

temp = changeColors(temp)
output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
print('Completed process in',(time.time()-previous),'seconds\n')

cv2.imshow('Input', img)
cv2.imshow('Output', output)

studs = {}
rows,cols = temp.shape[:2]

for i in range(rows):
    for j in range(cols):
        k = temp[i,j].tolist()
        for color in colors:
            if k == colors.get(color):
                if color in studs:
                    if studs.get(color) >= 1:
                        studs[color] += 1
                    else:
                        studs[color] = 1
                else:
                    studs[color] = 1
print('Studs required:')
print(json.dumps(studs,indent=3,sort_keys=True))

price = 0.08 * totalPixels
sizeW = 0.8 * int(w)
sizeH = 0.8 * int(h)

for i,c in enumerate(str(price)):
    if c == ".":
        price = str(price)[:i+3]
for i,c in enumerate(str(sizeW)):
    if c == ".":
        sizeW = str(sizeW)[:i+3]
for i,c in enumerate(str(sizeH)):
    if c == ".":
        sizeH = str(sizeH)[:i+3]

print(f"Your estimated total is ${price} CAD")
print(f"The size of your LEGO image will be {sizeW} cm by {sizeH} cm")

cv2.imwrite(str("LEGO " + name + ".jpg"), output)

cv2.waitKey(0)