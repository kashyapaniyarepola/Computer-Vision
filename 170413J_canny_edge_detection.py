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

def convolve(filter, image):
  lenFilter = len(filter)
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
      outRow.append(int(outEle))
      if (k+lenFilter == width):
        break
    outputImage.append(outRow)
    if (row+lenFilter == len(image)):
      break
    
  return outputImage

def sobel_filters(img):
    Kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    Ky = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

    wrappedLayer = getWrapped(img.tolist())
    
    Ix = numpy.array(convolve(Kx,img))
    Iy = numpy.array(convolve(Ky,img))
    
    G = numpy.hypot(Ix, Iy)
    G = G / G.max() * 255
    theta = numpy.arctan2(Iy, Ix)
    
    return (G, theta)

def non_max_suppression(img, D):
    M, N = img.shape
    Z = numpy.zeros((M,N), dtype=numpy.int32)
    angle = D * 180. / numpy.pi
    angle[angle < 0] += 180

    for i in range(1,M-1):
        for j in range(1,N-1):
            try:
                q = 255
                r = 255
                
               #angle 0
                if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                    q = img[i, j+1]
                    r = img[i, j-1]
                #angle 45
                elif (22.5 <= angle[i,j] < 67.5):
                    q = img[i+1, j-1]
                    r = img[i-1, j+1]
                #angle 90
                elif (67.5 <= angle[i,j] < 112.5):
                    q = img[i+1, j]
                    r = img[i-1, j]
                #angle 135
                elif (112.5 <= angle[i,j] < 157.5):
                    q = img[i-1, j-1]
                    r = img[i+1, j+1]

                if (img[i,j] >= q) and (img[i,j] >= r):
                    Z[i,j] = img[i,j]
                else:
                    Z[i,j] = 0

            except IndexError as e:
                pass
    
    return Z

def threshold(img, lowThresholdRatio=0.05, highThresholdRatio=0.09):
    
    highThreshold = img.max() * highThresholdRatio;
    lowThreshold = highThreshold * lowThresholdRatio;
    
    M, N = img.shape
    res = numpy.zeros((M,N), dtype=numpy.int32)
    
    weak = numpy.int32(25)
    strong = numpy.int32(255)
    
    strong_i, strong_j = numpy.where(img >= highThreshold)
    zeros_i, zeros_j = numpy.where(img < lowThreshold)
    
    weak_i, weak_j = numpy.where((img <= highThreshold) & (img >= lowThreshold))
    
    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak
    
    return (res, weak, strong)

def hysteresis(img, weak, strong=255):
    M, N = img.shape  
    for i in range(1, M-1):
        for j in range(1, N-1):
            if (img[i,j] == weak):
                try:
                    if ((img[i+1, j-1] == strong) or (img[i+1, j] == strong) or (img[i+1, j+1] == strong)
                        or (img[i, j-1] == strong) or (img[i, j+1] == strong)
                        or (img[i-1, j-1] == strong) or (img[i-1, j] == strong) or (img[i-1, j+1] == strong)):
                        img[i, j] = strong
                    else:
                        img[i, j] = 0
                except IndexError as e:
                    pass
    return img


imdir = ''
ext = ['jpeg', 'jpg']    # Image formats

files = []
[files.extend(glob.glob(imdir + '*.' + e)) for e in ext]

images = [cv2.imread(file,0) for file in files]

filter = [[1,1,1],[1,1,1],[1,1,1]]

for i in range(len(images)):
  fileName = files[i].split('.')[0]

  wrappedLayer = getWrapped(images[i].tolist())

  meanFilterLayer = getMeanFilterImage(filter,wrappedLayer)

  # sobel filter
  magnitide, direction = sobel_filters(numpy.array(meanFilterLayer))

  maxSup = non_max_suppression(magnitide, direction)

  res, weak, strong = threshold(maxSup)

  finalImage = hysteresis(res, weak, strong)
  
  cv2.imwrite(fileName +'- canny-edge-detection.jpeg', finalImage)
