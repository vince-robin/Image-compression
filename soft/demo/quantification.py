'''
Project Name: Image compression

Student: Vincent ROBIN, ENSTA Bretagne, promotion 2023
Contact: vincent.robin@ensta-bretagne.org

File name: quantification.py 
Create Date: 23/02/2023, 19:28:01 AM

Description: quantize each block of the picture. Visualisation of :
- the quantization error
- the quantised Y,Cr and Cb channels
- a randomly selected Y, Cr and Cb 8*8 quantised block in the image

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
    QLEVEL = 90
    QLuminance = quantization(QLEVEL, "luminance")
    QChrominance = quantization(QLEVEL, "chrominance")
    print("Quantization level is: ", QLEVEL)

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
    yq_error_acc = np.zeros((blockSize, blockSize))

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
            yq_error_acc += (yDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] - yq[row_ind_1:row_ind_2, col_ind_1:col_ind_2]*QLuminance)

    # Absolute quantization error introduce by the round() function
    yq_error = np.abs(yq_error_acc / (nbh * nbw))

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
    cbq_error_acc = np.zeros((blockSize, blockSize))
    crq_error_acc = np.zeros((blockSize, blockSize))

    for i in range(nbh_cbSub):
        row_ind_1 = i*blockSize
        row_ind_2 = row_ind_1+blockSize

        for j in range(nbw_cbSub):
            col_ind_1 = j*blockSize
            col_ind_2 = col_ind_1+blockSize

            crBlock = crPadded[row_ind_1:row_ind_2, col_ind_1:col_ind_2]
            crDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = (T.dot(crBlock)).dot(np.transpose(T))
            crq[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = np.round(crDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2]/ QChrominance)
            crq_error_acc += (crDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] - crq[row_ind_1:row_ind_2, col_ind_1:col_ind_2]*QChrominance)

            cbBlock = cbPadded[row_ind_1:row_ind_2, col_ind_1:col_ind_2]
            cbDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = (T.dot(cbBlock)).dot(np.transpose(T))
            cbq[row_ind_1:row_ind_2, col_ind_1:col_ind_2] = np.round(cbDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2]/ QChrominance)
            cbq_error_acc += (cbDct[row_ind_1:row_ind_2, col_ind_1:col_ind_2] - cbq[row_ind_1:row_ind_2, col_ind_1:col_ind_2]*QChrominance)

    # Absolute quantization error introduce by the round() function
    crq_error = np.abs(crq_error_acc / (nbh_cbSub * nbw_cbSub))
    cbq_error = np.abs(cbq_error_acc / (nbh_cbSub * nbw_cbSub))


    # **************************************************************** #
    #   Visualisation des canaux Y, Cr et Cb après la quantification   #
    # **************************************************************** #

    fig=plt.figure(figsize=(15,7.5))
    ax=fig.add_subplot(1,3,1)
    plt.title('Quantified Y - QLevel=' + str(QLEVEL))
    plt.imshow(np.uint8(yq),cmap='gray')
    fig.add_subplot(1,3,2)
    plt.title('Quantified Cr - QLevel=' + str(QLEVEL))
    plt.imshow(np.uint8(crq),cmap='gray')
    fig.add_subplot(1,3,3)
    plt.title('Quantified Cb - QLevel=' + str(QLEVEL))
    plt.imshow(np.uint8(cbq),cmap='gray')

    plt.show()

    # Sauvegarde de la figure 
    fig.savefig("quantization_error_QLevel_"+str(QLEVEL)+".png")

    # ********************************************************************** #
    #  Visualisation d'un bloc quantifié choisi au hasard pour Y, Cr et Cb   #
    # ***********************************************************************#

    i = np.random.randint(0, nbh-1)
    j = np.random.randint(0, nbw-1) 
    row_ind_1 = i*blockSize
    row_ind_2 = row_ind_1+blockSize
    col_ind_1 = j*blockSize
    col_ind_2 = col_ind_1+blockSize

    fig=plt.figure(figsize=(15,7.5))
    fig.add_subplot(1,3,1)
    plt.title('Y quantified')
    plt.imshow(yq[row_ind_1:row_ind_2, col_ind_1:col_ind_2],cmap='jet')
    plt.colorbar(shrink=0.5)

    i = np.random.randint(0, nbh_cbSub-1)
    j = np.random.randint(0, nbw_cbSub-1) 
    row_ind_1 = i*blockSize
    row_ind_2 = row_ind_1+blockSize
    col_ind_1 = j*blockSize
    col_ind_2 = col_ind_1+blockSize

    fig.add_subplot(1,3,2)
    plt.title('Cb quantified')
    plt.imshow(cbq[row_ind_1:row_ind_2, col_ind_1:col_ind_2],cmap='jet')
    plt.colorbar(shrink=0.5)

    fig.add_subplot(1,3,3)
    plt.title('Cr quantified')
    plt.imshow(crq[row_ind_1:row_ind_2, col_ind_1:col_ind_2],cmap='jet')
    plt.colorbar(shrink=0.5)

    plt.show()

    # Sauvegarde de la figure 
    fig.savefig("quantized_blocks_QLevel_"+str(QLEVEL)+".png")

    # ********************************************************************** #
    #   Visualisation de l'erreur de quantification moyenne pour Y, Cr et Cb #
    # ********************************************************************** #

    fig=plt.figure(figsize=(15,7.5))
    ax=fig.add_subplot(1,3,1)
    plt.title("Y : Erreur de quantification")
    plt.imshow(yq_error)
    plt.colorbar(shrink=0.5)
    ax=fig.add_subplot(1,3,2)
    plt.title("Cr : Erreur de quantification")
    plt.imshow(crq_error)
    plt.colorbar(shrink=0.5)
    ax=fig.add_subplot(1,3,3)
    plt.title("Cb : Erreur de quantification")
    plt.imshow(cbq_error)
    plt.colorbar(shrink=0.5)

    plt.show()

    # Sauvegarde de la figure 
    fig.savefig("channels_after_quantification_QLevel_"+str(QLEVEL)+".png")
    
