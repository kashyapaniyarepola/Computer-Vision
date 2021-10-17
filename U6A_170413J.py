import cv2
import glob
import numpy as np

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

def interMean(image):
    
  M, N = image.shape
  res = np.zeros((M,N), dtype=np.int32)
  weak = np.int32(0)
  strong = np.int32(255)

  initial_tresh = np.mean(image)
  partone_i, partone_j = np.where(image >= initial_tresh)
  parttwo_i, parttwo_j = np.where(image < initial_tresh)

  tresh = initial_tresh
  tresh_list = []
  tresh_list.append(initial_tresh)

  while (True):

    tot1 = 0
    tot2 = 0
    for i in range(partone_i.size):
      tot1 += image[partone_i[i]][partone_j[i]]
    
    for j in range(parttwo_i.size):
      tot2 += image[parttwo_i[j]][parttwo_j[j]]

    r1_mean = tot1/partone_i.size
    r2_mean = tot2/parttwo_i.size
    new_tresh = int((r1_mean+r2_mean)/2) 

    if (new_tresh == tresh_list[-1]):
      break
    elif (new_tresh in tresh_list):
      break
    else:
      partone_i, partone_j = np.where(image >= new_tresh)
      parttwo_i, parttwo_j = np.where(image < new_tresh)
      tresh_list.append(new_tresh)

  res[partone_i, partone_j] = strong
  res[parttwo_i, parttwo_j] = weak
  
  return res


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

  finalImage = interMean(np.array(meanFilterLayer))
  
  cv2.imwrite(fileName +'-inter-means.jpeg', finalImage)


# plt.show()
