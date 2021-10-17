
def getShinked(image):
  newRow = []
  for i in range(len(image[0])):
    newRow.append(0)
  
  image.insert(0,newRow)
  image.append(newRow)

  shrinkedImage = []
  for i in range(len(image)):
    shrinkedImage.append([0] + image[i] + [0])
  return shrinkedImage

def getPadded(image):
  newRowOne = []
  for i in range(len(image[0])):
    if (i%2==1):
        newRowOne.append(1)
    else:
        newRowOne.append(0)
            
  newRowTwo = []
  for i in range(len(image[0])):
    if (i%2==1):
        newRowTwo.append(0)
    else:
        newRowTwo.append(1)
  
  if (len(image)%2==0):
      image.insert(0,newRowOne)
      image.append(newRowTwo)
  else:
    image.insert(0,newRowOne)
    image.append(newRowOne)

  paddedImage = []
  for i in range(len(image)):
    w = 1
    b = 1
    if (i%2==0):
      if ((len(image[i]))%2==0):
        w = 1
        b = 0
      else:
        w = 1
        b = 1
    else:
      if ((len(image[i]))%2==0):
        w = 0
        b = 1
      else:
        w = 0
        b = 0
    paddedImage.append([w]+image[i]+[b]) 

  return paddedImage

def getReplicated(image):
  image.insert(0,image[0])
  image.append(image[-1])

  replicatedImage = []
  for i in range(len(image)):
    replicatedImage.append([image[i][0]] + image[i] + [image[i][-1]])
  return replicatedImage

def getWrapped(image):
  image.insert(0,image[-1])
  image.append(image[1])

  wrappedImage = []
  for i in range(len(image)):
    wrappedImage.append([image[i][-1]] + image[i] + [image[i][0]])
  return wrappedImage

def getFilterImage(filter, image):
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
      outRow.append(outEle)
      if (k+lenFilter == width):
        break
    outputImage.append(outRow)
    if (row+lenFilter == len(image)):
      break
    
  return outputImage

def linearFilter(filter, image, param):
  if (param == "O"):
    output = getFilterImage(filter,image)
  elif (param == "S"):
    output = getFilterImage(filter,getShinked(image))
  elif (param == "P"):
    output = getFilterImage(filter,getPadded(image))
  elif (param == "R"):
    output = getFilterImage(filter,getReplicated(image))
  elif (param == "W"):
    output = getFilterImage(filter,getWrapped(image))
  else:
    output = "Please enter valid parameter"
  
  return output

# input filter
filter_list = []
for j in range(3):
  input_string = input()
  filterRow = input_string.split()

  for i in range(len(filterRow)):
      filterRow[i] = int(filterRow[i])

  filter_list.append(filterRow)

# print(filter_list)

# input paramenter
param = input("Parameter Type: ").strip()
# print(param)

# input image as pixel matrix
image = []
N = input("Enter  number of rows (N): ")
N = int(N)
# N = 5
M= 5
for j in range(N):
  input_string = input()
  im = input_string.split()

  for i in range(len(im)):
      im[i] = int(im[i])

  image.append(im)

# print(image)

# filter = [[1,0,0],[1,1,0],[0,0,1]]
# image = [[3,5,2,8,1],[9,7,5,4,3],[2,0,6,1,6],[6,3,7,9,2],[1,4,9,5,1]]
# param = "P"

output = linearFilter(filter_list,image,param)
print(output)
