import cv2
import glob
import numpy

def getWrapped(image):
  # image.insert(0,image[-1])
  image.append(image[1])
  image.append(image[0])
  # image = [image[-1]]+image+[image[0]]
  wrappedImage = []
  for i in range(len(image)):
    # wrappedImage.append([image[i][-1]] + image[i] + [image[i][1]] + [image[i][0]])
    wrappedImage.append(image[i] + [image[i][1]] + [image[i][0]])
  return wrappedImage

def getMeanFilterImage(filter, image):
  lenFilter = len(filter)
  sizeOfFilter = lenFilter*lenFilter
  width = len(image[0])
  outputImage = []
  for row in range(len(image)):
    outRow = []
    for k in range(width):
      outEle = 0
      countR = 0
      for i in range(k,k+lenFilter):
        countC = 0
        for j in range(k,k+lenFilter):
          outEle += filter[countR][countC]*image[countR+row][j]
          countC +=1
        countR +=1
      outRow.append(int(outEle/sizeOfFilter))
      if (k+lenFilter == width):
        break
    outputImage.append(outRow)
    if (row+lenFilter == len(image)):
      break
    
  return outputImage

def getMedianFilterImage(filter, image):
  lenFilter = len(filter)
  width = len(image[0])
  outputImage = []
  for row in range(len(image)):
    outRow = []
    for k in range(width):
      outEle = 0
      countR = 0
      sortList = []
      for i in range(k,k+lenFilter):
        countC = 0
        for j in range(k,k+lenFilter):
          sortList.append(filter[countR][countC]*image[countR+row][j])
          countC +=1
        countR +=1
      sortList.sort()
      outEle = sortList[len(sortList)//2 +1]
      outRow.append(outEle)
      if (k+lenFilter == width):
        break
    outputImage.append(outRow)
    if (row+lenFilter == len(image)):
      break

  return outputImage

def getMidPointFilterImage(filter, image):
  lenFilter = len(filter)
  width = len(image[0])
  outputImage = []
  for row in range(len(image)):
    outRow = []
    for k in range(width):
      outEle = 0
      countR = 0
      sortList = []
      for i in range(k,k+lenFilter):
        countC = 0
        for j in range(k,k+lenFilter):
          sortList.append(filter[countR][countC]*image[countR+row][j])
          countC +=1
        countR +=1
      sortList.sort()
      outEle = int((sortList[0] + sortList[-1])/2)
      outRow.append(outEle)
      if (k+lenFilter == width):
        break
    outputImage.append(outRow)
    if (row+lenFilter == len(image)):
      break

  return outputImage

def splitImage(image):
    blue = []
    for i in range(len(image)):
        result = []
        for j in range(len(image[0])):
            result.append(image[i][j][0])
        blue.append(result)
    green = []
    for i in range(len(image)):
        result = []
        for j in range(len(image[1])):
            result.append(image[i][j][1])
        green.append(result)
    red = []
    for i in range(len(image)):
        result = []
        for j in range(len(image[2])):
            result.append(image[i][j][2])
        red.append(result)
        
    return blue,green,red

def mergeImage(b,g,r):
    
  mergedImage = []
  for i in range(len(b)):
      result = []
      for j in range(len(b[0])):
          result.append([b[i][j],g[i][j],r[i][j]])
      mergedImage.append(result)

  return mergedImage


imdir = ''
ext = ['jpeg', 'jpg']    # Add image formats here

files = []
[files.extend(glob.glob(imdir + '*.' + e)) for e in ext]

images = [cv2.imread(file) for file in files]

filter = [[1,1,1],[1,1,1],[1,1,1]]

for i in range(len(images)):
  fileName = files[i].split('.')[0]
  blue,green,red = splitImage(images[i])

  wrappedBlueLayer = getWrapped(blue)
  wrappedGreenLayer = getWrapped(green)
  wrappedRedLayer = getWrapped(red)

  meanFilterBlueLayer = getMeanFilterImage(filter,wrappedBlueLayer)
  meanFilterGreenLayer = getMeanFilterImage(filter,wrappedGreenLayer)
  meanFilterRedLayer = getMeanFilterImage(filter,wrappedRedLayer)
  
  meanFilterImage = mergeImage(meanFilterBlueLayer, meanFilterGreenLayer, meanFilterRedLayer)
  cv2.imwrite(fileName +'- Mean.jpeg', numpy.array(meanFilterImage))

  medianFilterBlueLayer = getMedianFilterImage(filter,wrappedBlueLayer)
  medianFilterGreenLayer = getMedianFilterImage(filter,wrappedGreenLayer)
  medianFilterRedLayer = getMedianFilterImage(filter,wrappedRedLayer)

  medianFilterImage = mergeImage(medianFilterBlueLayer, medianFilterGreenLayer, medianFilterRedLayer)
  cv2.imwrite(fileName +'- Median.jpeg', numpy.array(medianFilterImage))

  midpointFilterBlueLayer = getMidPointFilterImage(filter,wrappedBlueLayer)
  midpointFilterGreenLayer = getMidPointFilterImage(filter,wrappedGreenLayer)
  midpointFilterRedLayer = getMidPointFilterImage(filter,wrappedRedLayer)

  midpointFilterImage = mergeImage(midpointFilterBlueLayer, midpointFilterGreenLayer, midpointFilterRedLayer)
  cv2.imwrite(fileName +'- Mid-pont.jpeg', numpy.array(midpointFilterImage))





cv2.imwrite('myimage3.jpeg', newimg)
