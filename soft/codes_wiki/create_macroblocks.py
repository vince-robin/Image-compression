'''
Project Name: Image compression

Student: Vincent ROBIN, ENSTA Bretagne, promotion 2023
Contact: vincent.robin@ensta-bretagne.org

File name: create_macroblocks.py 
Create Date: 22/02/2023, 21:20:01 AM

Description: splits the original image into blocks of 8*8 pixels for luminance (Y) channel and,
if necessary, performs zero-padding for images whose dimensions cannot be divided by the block size.

Packages: 
  - matplotlib (pip install matplotlib)
  - numpy (pip install matplotlib)
  - pillow (pip install pillow)

Revision: Revision 0.01 - File Created
Additional Comments:

'''

import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

from PIL import Image, ImageDraw
from math import ceil


def rgb_to_ycrcb(im):
    
    xform = np.array([[.299, .587, .114], [.5, -.4187, -.0813], [-.1687, -.3313, .5]])
    ycbcr = im.dot(xform.T)
    ycbcr[:,:,[1,2]] += 128

    return np.uint8(ycbcr)


def show_macroblocks(image, h, w, blocksize):
    image=image[:h,:w]
    PIL_image = Image.fromarray(np.uint8(image))
    draw = ImageDraw.Draw(PIL_image)
    y_start = 0
    y_end = PIL_image.height

    for x in range(0, PIL_image.width, blocksize):
        line = ((x, y_start), (x, y_end))
        draw.line(line, fill=(255,255,255))

    x_start = 0
    x_end = PIL_image.width

    for y in range(0, PIL_image.height, blocksize):
        line = ((x_start, y), (x_end, y))
        draw.line(line, fill=(255,255,255))
    
    #print("Number of rows: {}, Number of cols: {}".format(int(y_end/blocksize),int(x_end/blocksize)))
    
    return PIL_image



if __name__ == '__main__':

    PATH ="img/baboon.jpg"
    img_rgb = img.imread(PATH)

    ### Conversion RGB --> YCrCb
    img_ycrcb = rgb_to_ycrcb(img_rgb)

    ### Extraction des canaux Y,Cr,Cb
    y =  img_ycrcb[:,:,0] 
    cr = img_ycrcb[:,:,1]  # Chrominance Red
    cb = img_ycrcb[:,:,2]  # Chrominance Blue

    ### Chroma subsampling (4:4:4 --> 4:2:2)
    crSub422 = cr[::2, ::2]
    cbSub422 = cb[::2, ::2]

    ### Chroma subsampling (4:2:2 --> 4:2:0)
    crSub420 = crSub422[::2, ::2]
    cbSub420 = cbSub422[::2, ::2]

    ### Zero Padding
    blockSize = 8
    h = y.shape[0]
    w = y.shape[1]
    nbh = ceil(h / blockSize)  # number of blocks in height and width : nbh et nbw
    nbw = ceil(w / blockSize)
    hPadded = blockSize * nbh  # height and width of padded image : hPadded, wPadded
    wPadded = blockSize * nbw

    print("Height: {0}, Width: {1}".format(h, w))
    print("Block size: ", blockSize)
    print("Number of blocks in height (nbh): ", nbh)
    print("Number of blocks in width (nbh): ", nbw)
    print("Height of padded image: ", hPadded)
    print("Width of padded image: ", wPadded)

    if (h % blockSize == 0) and (w % blockSize == 0):
        print("--> Zero padding is not required")
        yPadded = y.copy()
    else:
        print("--> Zero padding is required")
        yPadded = np.zeros((hPadded, wPadded))
        for i in range(h):
            for j in range(w):
                yPadded[i, j] += y[i, j]

    for i in range(nbh):
        row_ind_1 = i*blockSize
        row_ind_2 = row_ind_1+blockSize

        for j in range(nbw):
            col_ind_1 = j*blockSize
            col_ind_2 = col_ind_1+blockSize

            yBlock = yPadded[row_ind_1:row_ind_2, col_ind_1:col_ind_2]


    splitted_img = show_macroblocks(img_rgb, h, w, blockSize)

    fig=plt.figure(figsize=(10,6))
    fig.add_subplot(1, 2, 1)
    plt.title("Image split into blocks")
    plt.imshow(splitted_img)
    fig.add_subplot(1, 2, 2)
    plt.title("Last 8x8 block")
    plt.imshow(yBlock)

    # Ajustement de l'espacement entre les figures
    plt.subplots_adjust(wspace=0.5)

    # Sauvegarde de la figure 
    fig.savefig('blocks_visualization.png')

    plt.show()
    