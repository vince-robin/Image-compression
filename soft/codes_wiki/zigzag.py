'''
Project Name: Image compression

Student: Vincent ROBIN, ENSTA Bretagne, promotion 2023
Contact: vincent.robin@ensta-bretagne.org

File name: zigzag.py 
Create Date: 24/02/2023, 13:40:01 AM

Description: performs the readback of the 8*8 pixel quantized blocks in a "zigzag" sequence. 
Display of a quantised Cb chrominance block before and after zigzagging.

Packages: 
  - matplotlib (pip install matplotlib)
  - numpy (pip install matplotlib)

Revision: Revision 0.01 - File Created
Additional Comments:

'''

import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

from math import ceil, sqrt, cos, pi


QTY = np.array([
    [16, 11, 10, 16,  24,  40,  51,  61],  # luminance quantization table
    [12, 12, 14, 19,  26,  58,  60,  55],
    [14, 13, 16, 24,  40,  57,  69,  56],
    [14, 17, 22, 29,  51,  87,  80,  62],
    [18, 22, 37, 56,  68, 109, 103,  77],
    [24, 35, 55, 64,  81, 104, 113,  92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103,  99]])

QTC = np.array([
    [17, 18, 24, 47, 99, 99, 99, 99],  # chrominance quantization table
    [18, 21, 26, 66, 99, 99, 99, 99],
    [24, 26, 56, 99, 99, 99, 99, 99],
    [47, 66, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99]])


def rgb_to_ycrcb(im):
    
    xform = np.array([[.299, .587, .114], [.5, -.4187, -.0813], [-.1687, -.3313, .5]])
    ycbcr = im.dot(xform.T)
    ycbcr[:,:,[1,2]] += 128

    return np.uint8(ycbcr)


def compute_dct_coeffs():
    T = np.zeros((blockSize, blockSize))
    T[0, :] = sqrt(1.0/blockSize)
    for i in range(1, blockSize):
        for j in range(blockSize):
            T[i][j] = sqrt(2.0/blockSize)*cos(pi*(2.0*j+1.0)*i/(2.0*blockSize))

    return T


def quantization(QLevel, channel):

    if channel == 'luminance' : 
        Q_mat = QTY
    else:
        Q_mat = QTC
    if QLevel < 50 and QLevel > 1:
        Q = (50 / QLevel) * Q_mat
    elif QLevel < 100:
        Q = ((100 - QLevel) / 50) * Q_mat
    else:
        print("Quality Level must be in the range [1..99]")
    
    return np.uint8(Q) # value must be in the range 0 to 255


def constr_zigzag_table(vmax, hmax):
        
    h = 0
    v = 0
    vmin = 0
    hmin = 0
    zigzag_table = np.zeros((vmax, hmax))
    i = 0

    while ((v < vmax) and (h < hmax)): 
        if ((h + v) % 2) == 0:                 # going up
            if (v == vmin):				
                zigzag_table[v, h] = i        # if we got to the first line
                if (h == hmax):
                    v = v + 1
                else:
                    h = h + 1                        
                i = i + 1
            elif ((h == hmax -1 ) and (v < vmax)):   # if we got to the last column
                zigzag_table[v, h] = i 
                v = v + 1
                i = i + 1
            elif ((v > vmin) and (h < hmax -1 )):    # all other cases
                zigzag_table[v, h] = i 
                v = v - 1
                h = h + 1
                i = i + 1
        else:                                    # going down
            if ((v == vmax -1) and (h <= hmax -1)):       # if we got to the last line
                zigzag_table[v, h] = i 
                h = h + 1
                i = i + 1
            elif (h == hmin):                  # if we got to the first column
                zigzag_table[v, h] = i 
                if (v == vmax -1):
                    h = h + 1
                else:
                    v = v + 1
                i = i + 1        		
            elif((v < vmax -1) and (h > hmin)):     # all other cases
                zigzag_table[v, h] = i 
                v = v + 1
                h = h - 1
                i = i + 1

        if ((v == vmax-1) and (h == hmax-1)):          # bottom right element
            zigzag_table[v, h] = i 
            break
                
    return zigzag_table

def zigzag(input):

    h = 0
    v = 0
    v_min = 0
    h_min = 0
    v_max = input.shape[0]
    h_max = input.shape[1]
    i = 0
    output = np.zeros((v_max * h_max))

    while (v < v_max) and (h < h_max):

        if ((h + v) % 2) == 0:  # going up
            if v == v_min:
                output[i] = input[v, h]  # if we got to the first line
                if h == h_max:
                    v = v + 1
                else:
                    h = h + 1
                i = i + 1
            elif (h == h_max - 1) and (v < v_max):  # if we got to the last column
                output[i] = input[v, h]
                v = v + 1
                i = i + 1
            elif (v > v_min) and (h < h_max - 1):  # all other cases
                output[i] = input[v, h]
                v = v - 1
                h = h + 1
                i = i + 1
        else:

            if (v == v_max - 1) and (h <= h_max - 1):  # if we got to the last line
                output[i] = input[v, h]
                h = h + 1
                i = i + 1
            elif h == h_min:  # if we got to the first column
                output[i] = input[v, h]
                if v == v_max - 1:
                    h = h + 1
                else:
                    v = v + 1
                    i = i + 1
            elif (v < v_max - 1) and (h > h_min):  # all other cases
                output[i] = input[v, h]
                v = v + 1
                h = h - 1
                i = i + 1

        if (v == v_max - 1) and (h == h_max - 1):  # bottom right element
            output[i] = input[v, h]
            break

    return output



if __name__ == '__main__':

    PATH ="img/monster.jpg"
    img_rgb = img.imread(PATH)
    plt.imshow(img_rgb)
    plt.title("Image originale")
    plt.show()

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

    ### 64 DCT coefficients
    blockSize = 8
    T = compute_dct_coeffs()

    # Quantization matrix for luminance and chrominance with a defined quantization level QLEVEL
    # The higher the QLEVEL, the worse the compression, but the image quality remains.
    QLEVEL = 70
    QLuminance = quantization(QLEVEL, "luminance")
    QChrominance = quantization(QLEVEL, "chrominance")
    #print("Quantization level is: ", QLEVEL)


    # Construction of zig-zag table 
    zigzag_table = constr_zigzag_table(blockSize, blockSize)
    fig, ax = plt.subplots()
    ax.matshow(zigzag_table, cmap='viridis')
    for (i, j), z in np.ndenumerate(zigzag_table):
        ax.text(j, i, int(z), ha='center', va='center', color='black')
    plt.title("Zigzag-table")
    plt.show()

    # Sauvegarde de la figure 
    fig.savefig("zigzag_table.png")

    # ********************************************************#
    #                 PROCESS FOR LUMINANCE (Y)               #
    # ********************************************************#

    ### Zero Padding
    h = y.shape[0]
    w = y.shape[1]
    nbh = ceil(h / blockSize)  # number of blocks in height and width : nbh et nbw
    nbw = ceil(w / blockSize)
    hPadded = blockSize * nbh  # height and width of padded image : hPadded, wPadded
    wPadded = blockSize * nbw

    if (h % blockSize == 0) and (w % blockSize == 0):
        yPadded = y.copy()
    else:
        yPadded = np.zeros((hPadded, wPadded))
        for i in range(h):
            for j in range(w):
                yPadded[i, j] += y[i, j]

    yDct = np.zeros((hPadded, wPadded))
    yq = np.zeros((hPadded, wPadded))

    # DCT and Quantization
    for i in range(nbh):
        row_ind_1 = i*blockSize
        row_ind_2 = row_ind_1+blockSize

        for j in range(nbw):
            col_ind_1 = j*blockSize
            col_ind_2 = col_ind_1+blockSize

            yBlock = yPadded[row_ind_1:row_ind_2, col_ind_1:col_ind_2]
            yDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = (T.dot(yBlock)).dot(np.transpose(T))
            yq[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = np.round(yDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2]/ QLuminance)
            yZigzag = zigzag(yq[row_ind_1:row_ind_2, col_ind_1:col_ind_2])

    yZigzag = yZigzag.astype(np.int16)


    # ********************************************************#
    #             PROCESS FOR CHROMINANCE (Cr,CB)             #
    # ********************************************************#

    # Zero-padding
    h_cbSub = crSub420.shape[0] 
    w_cbSub = crSub420.shape[1] 
    nbh_cbSub = ceil(h_cbSub / blockSize)
    nbw_cbSub = ceil(w_cbSub / blockSize)
    hPadded_cbSub = blockSize * nbh_cbSub
    wPadded_cbSub  = blockSize * nbw_cbSub

    if (h_cbSub % blockSize == 0) and (w_cbSub % blockSize == 0):
        crPadded = crSub420.copy()
        cbPadded = cbSub420.copy()
    else:
        crPadded = np.zeros((hPadded_cbSub, wPadded_cbSub))
        cbPadded = np.zeros((hPadded_cbSub, wPadded_cbSub))
        for i in range(h_cbSub):
            for j in range(w_cbSub):
                crPadded[i, j] += crSub420[i, j]
                cbPadded[i, j] += cbSub420[i, j]

    # DCT and Quantization
    crDct = np.zeros((hPadded_cbSub, wPadded_cbSub))
    cbDct = np.zeros((hPadded_cbSub, wPadded_cbSub))
    crq = np.zeros((hPadded_cbSub, wPadded_cbSub))
    cbq = np.zeros((hPadded_cbSub, wPadded_cbSub))

    for i in range(nbh_cbSub):
        row_ind_1 = i*blockSize
        row_ind_2 = row_ind_1+blockSize

        for j in range(nbw_cbSub):
            col_ind_1 = j*blockSize
            col_ind_2 = col_ind_1+blockSize

            crBlock = crPadded[row_ind_1:row_ind_2, col_ind_1:col_ind_2]
            crDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = (T.dot(crBlock)).dot(np.transpose(T))
            crq[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = np.round(crDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2]/ QChrominance)
            crZigzag = zigzag(crq[row_ind_1:row_ind_2, col_ind_1:col_ind_2])

            cbBlock = cbPadded[row_ind_1:row_ind_2, col_ind_1:col_ind_2]
            cbDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = (T.dot(cbBlock)).dot(np.transpose(T))
            cbq[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = np.round(cbDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2]/ QChrominance)
            cbZigzag = zigzag(cbq[row_ind_1:row_ind_2, col_ind_1:col_ind_2])

    crZigzag = cbZigzag.astype(np.int16)
    cbZigzag = cbZigzag.astype(np.int16)

    # ****************************************************************** #
    # Visualisation d'un bloc de chrominance Cb avant et après zig-zag   #
    # ****************************************************************** #
   
    print("Before zig-zag: \n", cbq[row_ind_1:row_ind_2, col_ind_1:col_ind_2].astype(np.int16))
    print("\nAfter zig-zag: \n", cbZigzag)

    fig=plt.figure(figsize=(12,6))
    ax=fig.add_subplot(1,2,1)
    ax.matshow(cbq[row_ind_1:row_ind_2, col_ind_1:col_ind_2], cmap='viridis')
    for (ki, kj), z in np.ndenumerate(cbq[row_ind_1:row_ind_2, col_ind_1:col_ind_2]):
        ax.text(ki, kj, int(z), ha='center', va='center', color='black')
    plt.title("One chrominance block quantized")

    ax=fig.add_subplot(1,2,2)
    ax.plot(cbZigzag)
    #for ki, val in enumerate(cbZigzag):
        #ax.annotate(str(val), xy=(ki, val), xytext=(ki+0.1, val+0.1))
    plt.title("Zig-zag scan")
    plt.xlabel("Index")
    plt.ylabel("Zig zag value")

    plt.show()

    # Sauvegarde de la figure 
    fig.savefig("zigzag_one_block.png")
    

